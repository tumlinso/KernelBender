#!/usr/bin/env python3
"""Prepare and qualify the bounded KernelBender native pilot through KDA.

``prepare`` is CPU-only. ``qualify`` must be invoked only under the root-owned
KB-06 execution gate; it controller-admits sanitizer checks before it submits
any qualified candidate to KDA's existing controller-backed evaluator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PILOT_ROOT = ROOT / "runs" / "kernelbender-pilot"
RUNS_ROOT = PILOT_ROOT / "native-v1"
SITE_CONFIG = PILOT_ROOT / "site" / "controller.json"
KDA_ROOT = Path("/home/tumlinson/kda")
CUDA_ROOT = Path("/opt/nvidia/hpc_sdk/Linux_x86_64/26.1/cuda/12.9")
MATH_ROOT = Path("/opt/nvidia/hpc_sdk/Linux_x86_64/26.1/math_libs/12.9")
SANITIZER = CUDA_ROOT / "compute-sanitizer" / "compute-sanitizer"
SANITIZER_ADAPTER = Path("/home/tumlinson/kda/runs/attention-decode-study/workspace/site/sanitizer_tool.py")
CONTROLLER_ENTRY = Path("/home/tumlinson/kda/runs/attention-decode-study/workspace/site/controller_entry.py")
RUNTIME_IDENTITY = CONTROLLER_ENTRY.with_name("runtime-identity.json")
CUDA_CONTROLLER = Path("/home/tumlinson/.agents/skills/cuda/scripts/cuda_controller.py")
TRIAL_POLICY = ROOT / "evaluation" / "results" / "design-v1" / "trial-policy.json"
SOURCE_MANIFEST = ROOT / "evaluation" / "results" / "design-v1" / "shared-source-manifest.json"
AGENT_POLICY = ROOT / "evaluation" / "results" / "native-v1" / "agent-policy.json"
INPUT_MANIFESTS = ROOT / "evaluation" / "results" / "native-v1" / "input-manifests.json"
PRIVATE = ROOT / "evaluation" / "private"
NATIVE = ROOT / "evaluation" / "candidate" / "native"
FAMILIES = ("bool-transition", "observable-energy", "dense-gemm")
ARMS = ("A", "B")
SANITIZER_TOOLS = {
    "bool-transition": ("memcheck", "racecheck"),
    "observable-energy": ("memcheck", "racecheck"),
    "dense-gemm": ("memcheck", "racecheck"),
}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def tree_identity(root: Path) -> list[dict[str, str]]:
    records = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlinks are not accepted in candidate trees: {path}")
        if path.is_file():
            records.append({"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)})
    return records


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n",
                         encoding="utf-8")
    os.replace(temporary, path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_candidate_map(path: Path, run_id: str, policy: dict[str, Any]) -> dict[str, Any]:
    candidate_map = read_json(path)
    if not isinstance(candidate_map, dict) or candidate_map.get("schema_version") != 1:
        raise ValueError("candidate map must be a schema_version 1 object")
    if candidate_map.get("run_id") != run_id:
        raise ValueError("candidate map run_id must exactly match --run-id")
    declared_policy_hash = candidate_map.get("trial_policy_sha256")
    actual_policy_hash = sha256_file(TRIAL_POLICY)
    if declared_policy_hash != actual_policy_hash:
        raise ValueError("candidate map trial_policy_sha256 does not match the frozen trial policy")
    if candidate_map.get("source_manifest_sha256") != sha256_file(SOURCE_MANIFEST):
        raise ValueError("candidate map source_manifest_sha256 does not match the frozen shared source manifest")
    if candidate_map.get("agent_policy_sha256") != sha256_file(AGENT_POLICY):
        raise ValueError("candidate map agent_policy_sha256 does not match the staged native trial policy")
    if candidate_map.get("input_manifests_sha256") != sha256_file(INPUT_MANIFESTS):
        raise ValueError("candidate map input_manifests_sha256 does not match the staged trial inputs")
    if read_json(AGENT_POLICY).get("source_manifest_sha256") != sha256_file(SOURCE_MANIFEST):
        raise ValueError("staged native agent policy does not bind the expected shared source manifest")
    families = candidate_map.get("families")
    if not isinstance(families, dict) or set(families) != set(FAMILIES):
        raise ValueError(f"candidate map families must be exactly {list(FAMILIES)}")
    policy_limits = policy["stage_2"]
    max_builds = int(policy_limits["max_builds_per_agent"])
    max_candidates = int(policy_limits["max_candidates_per_agent"])
    for family in FAMILIES:
        family_record = families[family]
        if not isinstance(family_record, dict) or set(family_record) != set(ARMS):
            raise ValueError(f"{family} must contain explicit A and B records")
        for arm in ARMS:
            row = family_record[arm]
            if not isinstance(row, dict):
                raise ValueError(f"{family}/{arm} record must be an object")
            if row.get("outcome") not in {"candidate_ready", "no_candidate", "failed"}:
                raise ValueError(f"{family}/{arm} outcome must be candidate_ready, no_candidate, or failed")
            trial_id = row.get("trial_id")
            if not isinstance(trial_id, str) or not trial_id.strip():
                raise ValueError(f"{family}/{arm} must preserve a non-empty trial_id")
            count = row.get("build_attempts")
            if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= max_builds:
                raise ValueError(f"{family}/{arm} build_attempts exceeds the frozen limit {max_builds}")
            if row["outcome"] == "candidate_ready":
                if max_candidates < 1:
                    raise ValueError("frozen trial policy does not permit candidates")
                source = row.get("candidate_source")
                if not isinstance(source, dict) or not isinstance(source.get("source_dir"), str):
                    raise ValueError(f"{family}/{arm} ready outcome requires candidate_source.source_dir")
                manifest = source.get("manifest", "manifest.json")
                if not isinstance(manifest, str) or not manifest:
                    raise ValueError(f"{family}/{arm} candidate manifest must be a relative path")
                if Path(manifest).is_absolute() or ".." in Path(manifest).parts:
                    raise ValueError(f"{family}/{arm} candidate manifest must stay inside its source")
            elif row.get("candidate_source") is not None:
                raise ValueError(f"{family}/{arm} non-ready outcome must not register a candidate")
            evidence = row.get("attempt_records", [])
            if not isinstance(evidence, list):
                raise ValueError(f"{family}/{arm} attempt_records must be a list")
            kinds = set()
            for item in evidence:
                if (not isinstance(item, dict) or not isinstance(item.get("path"), str) or
                        item.get("kind") not in {"receipt", "commands", "briefs", "other"}):
                    raise ValueError(f"{family}/{arm} attempt record needs kind and path")
                kinds.add(item["kind"])
                if item.get("sha256") is not None and not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
                    raise ValueError(f"{family}/{arm} attempt record has malformed sha256")
            if not {"receipt", "commands"}.issubset(kinds):
                raise ValueError(f"{family}/{arm} must retain its command log and trial receipt")
    return candidate_map


def _record_command(run_dir: Path, label: str, argv: list[str], cwd: Path, *,
                    env: dict[str, str] | None = None, timeout: int = 300) -> dict[str, Any]:
    index = len((run_dir / "commands.jsonl").read_text().splitlines()) if (run_dir / "commands.jsonl").exists() else 0
    stem = f"{index:03d}-{label}"
    stdout_path = run_dir / "logs" / f"{stem}.stdout.txt"
    stderr_path = run_dir / "logs" / f"{stem}.stderr.txt"
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        completed = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True,
                                   timeout=timeout, check=False)
        returncode = completed.returncode
        stdout, stderr = completed.stdout, completed.stderr
        launch_error = None
    except subprocess.TimeoutExpired as exc:
        returncode = None
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        launch_error = f"TimeoutExpired after {timeout}s"
        stderr = stderr + ("\n" if stderr else "") + launch_error
    except Exception as exc:
        returncode = None
        stdout, stderr = "", f"{type(exc).__name__}: {exc}"
        launch_error = stderr
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    record = {
        "label": label, "argv": argv, "cwd": str(cwd), "returncode": returncode,
        "elapsed_seconds": time.monotonic() - started,
        "stdout_path": str(stdout_path), "stdout_sha256": sha256_file(stdout_path),
        "stderr_path": str(stderr_path), "stderr_sha256": sha256_file(stderr_path),
        "environment": {key: value for key, value in (env or {}).items()
                        if key in {"COMPUTE_SANITIZER_BIN", "KDA_SANITIZER_TOOL", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"}},
    }
    if launch_error:
        record["launch_error"] = launch_error
    try:
        output = json.loads(stdout)
        record["json_status"] = output.get("status") if isinstance(output, dict) else None
        record["json"] = output
    except (json.JSONDecodeError, ValueError):
        record["json_status"] = None
    with (run_dir / "commands.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True, allow_nan=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return record


def _require_command_ok(record: dict[str, Any], what: str) -> dict[str, Any]:
    if record["returncode"] != 0 or record.get("json_status") != "ok":
        raise RuntimeError(f"{what} failed: returncode={record['returncode']}, status={record.get('json_status')}")
    value = record.get("json")
    if not isinstance(value, dict):
        raise RuntimeError(f"{what} did not return a JSON object")
    return value


def _append_task_trusted_inputs(task_path: Path) -> None:
    task = read_json(task_path)
    additions = [
        ("native_pilot_driver", Path(__file__), "harness"),
        ("sanitizer_policy_adapter", SANITIZER_ADAPTER, "toolchain"),
        ("compute_sanitizer_cuda_12_9", SANITIZER, "toolchain"),
        ("nvcc_cuda_12_9", CUDA_ROOT / "bin" / "nvcc", "toolchain"),
        ("cuda_runtime_12_9", CUDA_ROOT / "lib64" / "libcudart.so", "toolchain"),
        ("cublas_12_9", MATH_ROOT / "lib64" / "libcublas.so", "toolchain"),
        ("frozen_trial_policy", TRIAL_POLICY, "other"),
        ("frozen_shared_source_manifest", SOURCE_MANIFEST, "other"),
        ("native_agent_policy", AGENT_POLICY, "other"),
        ("native_trial_input_manifests", INPUT_MANIFESTS, "other"),
        ("capture_setup_reference", SANITIZER_ADAPTER.with_name("capture_setup.py"), "other"),
    ]
    ids = {item["id"] for item in task["trusted_inputs"]}
    for item_id, path, role in additions:
        if not path.is_file():
            raise FileNotFoundError(path)
        if item_id not in ids:
            task["trusted_inputs"].append({"id": item_id, "path": str(path.resolve()), "role": role})
    write_json(task_path, task)


def _materialize(run_dir: Path, family: str) -> Path:
    cuda_lib = CUDA_ROOT / "lib64"
    cublas_lib = MATH_ROOT / "lib64"
    argv = [
        sys.executable, str(PRIVATE / "materialize_tasks.py"), family,
        "--output", str(run_dir / "tasks" / family), "--site-config", str(SITE_CONFIG),
        "--kda-root", str(KDA_ROOT), "--nvcc", str(CUDA_ROOT / "bin" / "nvcc"),
        "--cuda-lib-dir", str(cuda_lib), "--cublas-lib-dir", str(cublas_lib),
        "--controller-entry", str(CONTROLLER_ENTRY), "--runtime-identity", str(RUNTIME_IDENTITY),
        "--cuda-controller-script", str(CUDA_CONTROLLER),
    ]
    result = _record_command(run_dir, f"materialize-{family}", argv, ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(f"materialize {family} failed: {result['stderr_path']}")
    task_path = run_dir / "tasks" / family / "task.json"
    _append_task_trusted_inputs(task_path)
    return task_path


def _retain_attempt_records(run_dir: Path, family: str, arm: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    retained = []
    for index, item in enumerate(rows):
        source = Path(item["path"]).resolve(strict=True)
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"attempt evidence must be a regular file: {source}")
        actual = sha256_file(source)
        expected = item.get("sha256")
        if expected is not None and expected != actual:
            raise ValueError(f"attempt evidence hash changed: {source}")
        target = run_dir / "trial-evidence" / family / arm / f"{index:03d}-{source.name}"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        retained.append({"kind": item["kind"], "source_path": str(source), "source_sha256": actual,
                         "retained_path": str(target), "retained_sha256": sha256_file(target)})
    return retained


def _stage_source(run_dir: Path, family: str, arm: str, source: dict[str, Any]) -> tuple[Path, Path, list[dict[str, str]]]:
    original = Path(source["source_dir"]).resolve(strict=True)
    if not original.is_dir() or original.is_symlink():
        raise ValueError(f"candidate source_dir must be a real directory: {original}")
    tree_identity(original)
    manifest_rel = Path(source.get("manifest", "manifest.json"))
    manifest_source = original / manifest_rel
    if not manifest_source.is_file() or manifest_source.is_symlink():
        raise ValueError(f"candidate manifest is missing or unsafe: {manifest_source}")
    api = NATIVE / family / "candidate_api.h"
    candidate_api = original / "candidate_api.h"
    if not candidate_api.is_file() or candidate_api.is_symlink() or candidate_api.read_bytes() != api.read_bytes():
        raise ValueError(f"candidate {family}/{arm} candidate_api.h differs from the frozen ABI")
    target = run_dir / "sources" / family / arm
    if target.exists():
        raise FileExistsError(target)
    shutil.copytree(original, target, symlinks=False)
    copied_manifest = target / manifest_rel
    copied_manifest_value = read_json(copied_manifest)
    if copied_manifest_value.get("schema_version") != 1:
        raise ValueError(f"candidate {family}/{arm} manifest schema_version must equal 1")
    manifest_files = copied_manifest_value.get("files")
    if not isinstance(manifest_files, list) or not manifest_files:
        raise ValueError(f"candidate {family}/{arm} manifest.files must be a non-empty list")
    if not {"candidate_api.h", "kernel.cu"}.issubset(set(manifest_files)):
        raise ValueError(f"candidate {family}/{arm} manifest must declare candidate_api.h and kernel.cu")
    for relative in manifest_files:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or not (target / path).is_file() or (target / path).is_symlink():
            raise ValueError(f"candidate {family}/{arm} contains an invalid declared file: {relative}")
    return target, copied_manifest, tree_identity(target)


def _kda_argv(task_path: Path, workspace: Path, args: list[str]) -> list[str]:
    return [sys.executable, "-m", "kda_experiments", "--task", str(task_path),
            "--workspace", str(workspace), *args]


def prepare(run_id: str, candidate_map_path: Path) -> Path:
    if not ID_PATTERN.fullmatch(run_id):
        raise ValueError("run_id must be a simple filesystem-safe identifier")
    policy = read_json(TRIAL_POLICY)
    candidate_map_path = candidate_map_path.resolve(strict=True)
    candidate_map = _validate_candidate_map(candidate_map_path, run_id, policy)
    if not SITE_CONFIG.is_file():
        raise FileNotFoundError(SITE_CONFIG)
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    copied_map = run_dir / "candidate-map.json"
    shutil.copyfile(candidate_map_path, copied_map)
    state: dict[str, Any] = {
        "schema_version": 1, "run_id": run_id, "status": "preparing",
        "candidate_map": str(copied_map), "candidate_map_sha256": sha256_file(copied_map),
        "trial_policy": str(TRIAL_POLICY), "trial_policy_sha256": sha256_file(TRIAL_POLICY),
        "source_manifest": str(SOURCE_MANIFEST), "source_manifest_sha256": sha256_file(SOURCE_MANIFEST),
        "agent_policy": str(AGENT_POLICY), "agent_policy_sha256": sha256_file(AGENT_POLICY),
        "input_manifests": str(INPUT_MANIFESTS), "input_manifests_sha256": sha256_file(INPUT_MANIFESTS),
        "driver": str(Path(__file__).resolve()), "driver_sha256": sha256_file(Path(__file__).resolve()),
        "site_config": str(SITE_CONFIG), "site_config_sha256": sha256_file(SITE_CONFIG),
        "families": {},
    }
    write_json(run_dir / "run.json", state)
    try:
        for family in FAMILIES:
            task_path = _materialize(run_dir, family)
            family_workspace = run_dir / "work" / family
            family_workspace.mkdir(parents=True, exist_ok=False)
            family_state: dict[str, Any] = {
                "status": "preparing", "task": str(task_path), "task_sha256": sha256_file(task_path),
                "workspace": str(family_workspace), "task_id": read_json(task_path)["task_id"],
                "candidates": {},
            }
            state["families"][family] = family_state
            write_json(run_dir / "run.json", state)
            source_baseline = run_dir / "sources" / family / "baseline"
            source_baseline.mkdir(parents=True, exist_ok=False)
            shutil.copyfile(NATIVE / family / "baseline" / "kernel.cu", source_baseline / "kernel.cu")
            shutil.copyfile(NATIVE / family / "candidate_api.h", source_baseline / "candidate_api.h")
            baseline_manifest = source_baseline / "manifest.json"
            write_json(baseline_manifest, {"schema_version": 1,
                                           "files": ["candidate_api.h", "kernel.cu"],
                                           "dependencies": []})
            candidates: dict[str, Any] = {"baseline": {"status": "unregistered"}}
            family_state["candidates"] = candidates
            write_json(run_dir / "run.json", state)
            register_items: list[tuple[str, Path, Path, bool]] = [("baseline", source_baseline, baseline_manifest, True)]
            trial_rows = candidate_map["families"][family]
            for arm in ARMS:
                row = trial_rows[arm]
                copied_records = _retain_attempt_records(run_dir, family, arm, row.get("attempt_records", []))
                item: dict[str, Any] = {"trial_id": row["trial_id"], "outcome": row["outcome"],
                                        "build_attempts": row["build_attempts"],
                                        "attempt_records": copied_records, "status": row["outcome"]}
                if row["outcome"] == "candidate_ready":
                    source, manifest, identity = _stage_source(run_dir, family, arm, row["candidate_source"])
                    item.update({"source_dir": str(source), "manifest": str(manifest),
                                 "source_identity": identity,
                                 "source_sha256": canonical_hash(identity)})
                    register_items.append((f"candidate-{arm.lower()}", source, manifest, False))
                candidates[f"candidate-{arm.lower()}"] = item
                write_json(run_dir / "run.json", state)
            for candidate_id, source, manifest, is_baseline in register_items:
                hypothesis = "corrected conventional baseline" if is_baseline else f"design-trial candidate from {candidate_id}"
                change = "reviewed corrected native baseline" if is_baseline else "candidate from frozen independent design trial"
                argv = _kda_argv(task_path, family_workspace,
                                 ["register", candidate_id, str(source), "--manifest", str(manifest),
                                  "--hypothesis", hypothesis, "--change", change] + (["--baseline"] if is_baseline else []))
                record = _record_command(run_dir, f"register-{family}-{candidate_id}", argv, KDA_ROOT,
                                         env={**os.environ, "OPENBLAS_NUM_THREADS": "2", "OMP_NUM_THREADS": "2"})
                try:
                    result = _require_command_ok(record, f"KDA register {family}/{candidate_id}")
                    registered = result.get("candidate")
                    if not isinstance(registered, dict):
                        raise RuntimeError("KDA register omitted candidate record")
                    candidates[candidate_id].update({"status": "registered", "record": registered,
                                                     "registered_source_sha256": registered.get("snapshot_sha256")})
                except Exception as exc:
                    candidates[candidate_id].update({"status": "register_failed", "failure": str(exc)})
                    if not is_baseline:
                        candidates[candidate_id]["outcome"] = "failed"
                write_json(run_dir / "run.json", state)
            registered_ids = [candidate_id for candidate_id, *_ in register_items
                              if candidates[candidate_id].get("status") == "registered"]
            if registered_ids:
                argv = _kda_argv(task_path, family_workspace, ["prepare", *registered_ids, "--jobs", "1"])
                record = _record_command(run_dir, f"prepare-{family}", argv, KDA_ROOT,
                                         env={**os.environ, "OPENBLAS_NUM_THREADS": "2", "OMP_NUM_THREADS": "2"},
                                         timeout=1200)
                response = record.get("json") if isinstance(record.get("json"), dict) else {}
                build_results = {item.get("candidate_id"): item for item in response.get("results", [])
                                 if isinstance(item, dict)}
                for candidate_id in registered_ids:
                    result = build_results.get(candidate_id, {})
                    candidates[candidate_id]["prepare"] = result
                    candidates[candidate_id]["status"] = "prepared" if result.get("status") == "ok" else "build_failed"
                    if result.get("status") != "ok" and candidate_id.startswith("candidate-"):
                        candidates[candidate_id]["outcome"] = "failed"
                if record["returncode"] not in (0, 1) or not response:
                    for candidate_id in registered_ids:
                        if candidates[candidate_id]["status"] != "prepared":
                            candidates[candidate_id].setdefault("failure", "KDA prepare did not return a usable build result")
            family_failed = candidates["baseline"].get("status") != "prepared"
            family_status = "baseline_build_failed" if family_failed else "prepared"
            state["families"][family] = {
                "status": family_status, "task": str(task_path), "task_sha256": sha256_file(task_path),
                "workspace": str(family_workspace), "task_id": read_json(task_path)["task_id"],
                "candidates": candidates,
            }
            write_json(run_dir / "run.json", state)
        state["status"] = "prepared" if all(x["status"] == "prepared" for x in state["families"].values()) else "prepared_with_failures"
        write_json(run_dir / "run.json", state)
    except Exception as exc:
        state["status"] = "prepare_failed"
        state["error"] = f"{type(exc).__name__}: {exc}"
        write_json(run_dir / "run.json", state)
        raise
    return run_dir


def _workload_descriptor(case: dict[str, Any]) -> dict[str, Any]:
    descriptor = {key: value for key, value in case.items() if key != "workload_sha256"}
    return {**descriptor, "workload_sha256": canonical_hash(descriptor)}


def _artifact_identities(candidate: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    record = candidate.get("record")
    build = candidate.get("prepare")
    if not isinstance(record, dict) or not isinstance(build, dict) or build.get("status") != "ok":
        raise ValueError("candidate lacks successful KDA registration/build records")
    source_root = Path(record["snapshot_dir"]).resolve(strict=True)
    source_files = tree_identity(source_root)
    if canonical_hash(source_files) != canonical_hash(candidate.get("source_identity")) and candidate.get("source_identity") is not None:
        # Candidate records bind to KDA's canonical file manifest, whose file
        # set excludes unlisted extras. The exact declared source is checked
        # below and its digest is the recorded KDA snapshot identity.
        declared = record.get("source_manifest", [])
        if any(sha256_file(source_root / item["path"]) != item["sha256"] for item in declared):
            raise ValueError("KDA candidate snapshot no longer matches its registered source")
    directory = Path(build["directory"]).resolve(strict=True)
    artifacts = []
    for artifact in build.get("artifacts", []):
        path = directory / artifact["path"]
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"prepared artifact missing or unsafe: {path}")
        actual = sha256_file(path)
        if actual != artifact.get("sha256"):
            raise ValueError(f"prepared artifact digest mismatch: {path}")
        artifacts.append({"path": str(path), "sha256": actual})
    if len([item for item in artifacts if item["path"].endswith(".so")]) != 1:
        raise ValueError("native runner requires exactly one prepared shared library")
    request_candidate = {
        "id": record["candidate_id"], "snapshot_sha256": record["snapshot_sha256"],
        "source_dir": record["snapshot_dir"], "dependencies": record.get("dependencies", []),
        "build": {key: build[key] for key in ("directory", "fingerprint", "artifacts")},
    }
    return request_candidate, artifacts


def _validate_runner_json(result_path: Path, task: dict[str, Any], request_id: str) -> dict[str, Any]:
    if not result_path.is_file():
        raise ValueError("native evaluator result JSON was not produced")
    result = read_json(result_path)
    if result.get("schema_version") != 1 or result.get("request_id") != request_id:
        raise ValueError("native evaluator result identity does not match the request")
    case_hashes = {case["id"]: _workload_descriptor(case)["workload_sha256"] for case in task["cases"]}
    rows = result.get("cases")
    if not isinstance(rows, list):
        raise ValueError("native evaluator result cases must be an array")
    seen: dict[str, str] = {}
    for row in rows:
        case_id = row.get("case_id")
        if case_id not in case_hashes or case_id in seen:
            raise ValueError(f"native evaluator returned unexpected or duplicate case {case_id!r}")
        if row.get("workload_sha256") != case_hashes[case_id]:
            raise ValueError(f"native evaluator workload hash mismatch for {case_id}")
        seen[case_id] = row.get("status")
    if set(seen) != set(case_hashes):
        raise ValueError("native evaluator omitted one or more public cases")
    private_status = result.get("private_checks", {}).get("status")
    passed = result.get("status") == "ok" and private_status == "pass" and all(status == "pass" for status in seen.values())
    return {"status": "passed" if passed else "failed", "result": result,
            "public_case_status": seen, "private_status": private_status}


def _parse_sanitizer_artifacts(controller_record: dict[str, Any], tool: str) -> dict[str, Any]:
    receipt = controller_record.get("json")
    if not isinstance(receipt, dict):
        raise ValueError("controller did not return a receipt JSON object")
    stdout_path = receipt.get("stdout_path")
    stderr_path = receipt.get("stderr_path")
    if not isinstance(stdout_path, str) or not Path(stdout_path).is_file():
        raise ValueError("controller receipt lacks an existing stdout artifact")
    output = Path(stdout_path).read_text(encoding="utf-8", errors="replace")
    raw_matches = re.findall(r"^- raw log: (.+)$", output, flags=re.MULTILINE)
    summary_matches = re.findall(r"^Compute Sanitizer summary: (.+)$", output, flags=re.MULTILINE)
    if not raw_matches or not summary_matches:
        raise ValueError("controller stdout does not identify sanitizer raw log and summary")
    raw_log, summary_text = Path(raw_matches[-1]), Path(summary_matches[-1])
    if not raw_log.is_file() or not summary_text.is_file():
        raise ValueError("sanitizer raw log or summary artifact is missing")
    raw = raw_log.read_text(encoding="utf-8", errors="replace")
    if tool == "memcheck":
        parsed_summaries = [
            {"errors": int(errors)}
            for errors in re.findall(r"ERROR SUMMARY:\s*(\d+)\s+errors?", raw, flags=re.IGNORECASE)
        ]
    elif tool == "racecheck":
        parsed_summaries = [
            {"hazards": int(hazards), "errors": int(errors), "warnings": int(warnings)}
            for hazards, errors, warnings in re.findall(
                r"RACECHECK SUMMARY:\s*(\d+)\s+hazards? displayed\s*"
                r"\((\d+)\s+errors?,\s*(\d+)\s+warnings?\)",
                raw, flags=re.IGNORECASE)
        ]
    else:
        raise ValueError(f"unsupported sanitizer summary format: {tool}")
    summary_json = summary_text.with_suffix(".json")
    parsed_summary = read_json(summary_json) if summary_json.is_file() else None
    target_exit_status = (parsed_summary.get("exit_status")
                          if isinstance(parsed_summary, dict) else None)
    target_succeeded = (isinstance(target_exit_status, int) and
                        not isinstance(target_exit_status, bool) and target_exit_status == 0)
    return {
        "controller_receipt": receipt, "controller_stdout_path": stdout_path,
        "controller_stdout_sha256": sha256_file(Path(stdout_path)),
        "controller_stderr_path": stderr_path,
        "raw_log_path": str(raw_log), "raw_log_sha256": sha256_file(raw_log),
        "sanitizer_tool": tool,
        "sanitizer_summaries": parsed_summaries,
        "error_summary_counts": [summary["errors"] for summary in parsed_summaries],
        "summary_path": str(summary_text), "summary_sha256": sha256_file(summary_text),
        "summary_json_path": str(summary_json) if summary_json.is_file() else None,
        "summary_json": parsed_summary,
        "target_exit_status": target_exit_status,
        "passed": (bool(parsed_summaries) and
                   all(all(value == 0 for value in summary.values())
                       for summary in parsed_summaries) and target_succeeded),
    }


def _controller_succeeded(record: dict[str, Any]) -> bool:
    receipt = record.get("json")
    return bool(record.get("returncode") == 0 and isinstance(receipt, dict) and
                record.get("json_status") == "succeeded" and receipt.get("ok") is True and
                receipt.get("status") == "succeeded")


def _controller_spec(run_dir: Path, family: str, candidate_id: str, tool: str,
                     task_path: Path, request_path: Path, result_path: Path,
                     build_artifact: str) -> Path:
    config = read_json(SITE_CONFIG)
    validation_dir = result_path.parent
    validation_dir.mkdir(parents=True, exist_ok=True)
    runner = PRIVATE / "native_runner.py"
    arguments = [sys.executable, str(runner), "validate", "--family", family,
                 "--references", str(PRIVATE / "references.py"),
                 "--holdouts", str(PRIVATE / "holdouts.json"),
                 "--cuda-lib-dir", str(CUDA_ROOT / "lib64"),
                 "--cublas-lib-dir", str(MATH_ROOT / "lib64"),
                 "--nvcc", str(CUDA_ROOT / "bin" / "nvcc"),
                 str(request_path), str(result_path)]
    project = Path(config["project_root"]).resolve()
    try:
        binary_rel = Path(build_artifact).resolve().relative_to(project).as_posix()
    except ValueError as exc:
        raise ValueError("build artifact must be inside the configured pilot project root") from exc
    spec = {
        "schema_version": 1,
        "project_root": config["project_root"],
        "command_cwd": str(run_dir.resolve()),
        "recipe": "compute-sanitizer",
        "toolchain": {"root": config["toolchain"]["root"], "require_sanitizer": True},
        "resources": config["resources"],
        "quiescence": config.get("quiescence", {}),
        "timeout": 900,
        "argv": arguments,
        "binary_paths": [binary_rel],
        "paths": ["evaluation/candidate/native", "evaluation/private",
                  "evaluation/results/native-v1/driver.py"],
        "campaign_id": f"kernelbender-native-{family}-{candidate_id}-{tool}",
        "diagnostic_policy": {
            "purpose": "correctness qualification before timing credit",
            "family": family, "candidate_id": candidate_id,
            "selected_sanitizer": tool,
            "sanitizer_adapter": str(SANITIZER_ADAPTER),
            "sanitizer_adapter_sha256": sha256_file(SANITIZER_ADAPTER),
            "actual_sanitizer": str(SANITIZER),
            "actual_sanitizer_sha256": sha256_file(SANITIZER),
            "task_sha256": sha256_file(task_path),
            "request_sha256": sha256_file(request_path),
            "build_artifact": build_artifact,
            "build_artifact_sha256": sha256_file(Path(build_artifact)),
        },
    }
    spec_path = result_path.parent / "controller-spec.json"
    write_json(spec_path, spec)
    return spec_path


def _qualify_one(run_dir: Path, family: str, candidate_id: str,
                 candidate: dict[str, Any], task_path: Path, task: dict[str, Any]) -> dict[str, Any]:
    request_candidate, artifacts = _artifact_identities(candidate)
    build_artifact = next(item["path"] for item in artifacts if item["path"].endswith(".so"))
    candidate_dir = run_dir / "qualification" / family / candidate_id
    candidate_dir.mkdir(parents=True, exist_ok=False)
    results: list[dict[str, Any]] = []
    request_id = uuid.uuid4().hex
    request = {
        "schema_version": 1, "request_id": request_id, "operation": "validate",
        "task_id": task["task_id"], "target": task["target"],
        "candidate": request_candidate,
        "cases": [_workload_descriptor(case) for case in task["cases"]],
        "numerical_requirements": task["numerical_requirements"],
        "environment": {"qualification": "controller_admitted_compute_sanitizer"},
    }
    request_path = candidate_dir / "validation-request.json"
    result_path = candidate_dir / "validation-result.json"
    write_json(request_path, request)
    source_before = tree_identity(Path(request_candidate["source_dir"]))
    binary_before = sha256_file(Path(build_artifact))
    for tool in SANITIZER_TOOLS[family]:
        tool_dir = candidate_dir / tool
        tool_dir.mkdir()
        tool_result = tool_dir / "validation-result.json"
        shutil.copyfile(request_path, tool_dir / "validation-request.json")
        spec_path = _controller_spec(run_dir, family, candidate_id, tool, task_path,
                                     tool_dir / "validation-request.json", tool_result, build_artifact)
        config = read_json(SITE_CONFIG)
        argv = [*config["controller_argv"], "run", "--spec", str(spec_path), "--json"]
        env = os.environ.copy()
        env.update({"COMPUTE_SANITIZER_BIN": str(SANITIZER_ADAPTER),
                    "KDA_SANITIZER_TOOL": tool,
                    "OPENBLAS_NUM_THREADS": "2", "OMP_NUM_THREADS": "2"})
        controller_record = _record_command(run_dir, f"sanitize-{family}-{candidate_id}-{tool}",
                                            argv, ROOT, env=env, timeout=1200)
        response = {"tool": tool, "controller": controller_record}
        try:
            parsed = _parse_sanitizer_artifacts(controller_record, tool)
            response["sanitizer"] = parsed
            request_result = _validate_runner_json(tool_result, task, request_id)
            response["validation"] = request_result
            response["passed"] = bool(_controller_succeeded(controller_record) and
                                       parsed["passed"] and request_result["status"] == "passed")
            if not response["passed"]:
                response["failure"] = "controller, sanitizer log, or independent public/private validation failed"
        except Exception as exc:
            response["passed"] = False
            response["failure"] = f"{type(exc).__name__}: {exc}"
        results.append(response)
    source_after = tree_identity(Path(request_candidate["source_dir"]))
    binary_after = sha256_file(Path(build_artifact))
    passed = (all(item["passed"] for item in results) and source_before == source_after and
              binary_before == binary_after)
    return {
        "status": "qualified" if passed else "qualification_failed",
        "candidate_id": candidate_id, "snapshot_sha256": request_candidate["snapshot_sha256"],
        "build_fingerprint": request_candidate["build"]["fingerprint"],
        "artifacts": artifacts, "source_identity_before": source_before,
        "source_identity_after": source_after, "binary_sha256_before": binary_before,
        "binary_sha256_after": binary_after, "sanitizers": results,
    }


def _terminal_success(state: dict[str, Any]) -> bool:
    families = state.get("families", {})
    if set(families) != set(FAMILIES):
        return False
    for record in families.values():
        candidates = record.get("candidates", {})
        baseline = candidates.get("baseline", {})
        if baseline.get("qualification", {}).get("status") != "qualified":
            return False
        qualified = [name for name in ("candidate-a", "candidate-b")
                     if candidates.get(name, {}).get("qualification", {}).get("status") == "qualified"]
        if record.get("status") == "no_qualified_candidate":
            if qualified or record.get("qualified_candidates") != ["baseline"] or record.get("timing_status") != "not_run":
                return False
            continue
        if record.get("status") != "evaluated" or record.get("timing_status") != "complete" or not qualified:
            return False
        evaluation = record.get("evaluation", {})
        result = evaluation.get("json", {})
        expected = ["baseline", *qualified]
        if (evaluation.get("returncode") != 0 or evaluation.get("json_status") != "ok" or
                result.get("engine_status") != "complete" or
                not isinstance(result.get("run_id"), str) or not result["run_id"] or
                record.get("qualified_candidates") != expected):
            return False
        summary_path = result.get("summary_path")
        if not isinstance(summary_path, str) or not Path(summary_path).is_file():
            return False
        summary = read_json(Path(summary_path))
        validation = summary.get("validation", {})
        if (summary.get("status") != "complete" or summary.get("run_id") != result["run_id"] or
                any(validation.get(name, {}).get("status") != "pass" for name in expected) or
                summary.get("benchmark_failures")):
            return False
        confirmation = summary.get("confirmation")
        if isinstance(confirmation, dict) and confirmation.get("failures"):
            return False
    return True


def qualify(run_id: str) -> Path:
    if not ID_PATTERN.fullmatch(run_id):
        raise ValueError("run_id must be a simple filesystem-safe identifier")
    run_dir = RUNS_ROOT / run_id
    state_path = run_dir / "run.json"
    state = read_json(state_path)
    if state.get("run_id") != run_id or state.get("status") != "prepared":
        raise ValueError("qualify requires a matching run with status=prepared")
    if state.get("driver_sha256") != sha256_file(Path(__file__).resolve()):
        raise ValueError("driver source changed since CPU preparation; bind and prepare a new run")
    state["status"] = "qualifying"
    write_json(state_path, state)
    for family in FAMILIES:
        record = state["families"][family]
        if record["status"] != "prepared":
            record["status"] = "baseline_build_failed"
            record["timing_status"] = "blocked"
            record["reason"] = "baseline did not prepare successfully"
            write_json(state_path, state)
            continue
        task_path = Path(record["task"])
        task = read_json(task_path)
        candidates = record["candidates"]
        baseline = candidates.get("baseline", {})
        if baseline.get("status") != "prepared":
            record["status"] = "baseline_build_failed"
            record["timing_status"] = "blocked"
            write_json(state_path, state)
            continue
        baseline_result = _qualify_one(run_dir, family, "baseline", baseline, task_path, task)
        baseline["qualification"] = baseline_result
        if baseline_result["status"] != "qualified":
            record["status"] = "baseline_qualification_failed"
            record["timing_status"] = "blocked"
            record["failure"] = "baseline failed sanitizer/public/private correctness qualification"
            write_json(state_path, state)
            continue
        qualified_ids = ["baseline"]
        for candidate_id in ("candidate-a", "candidate-b"):
            candidate = candidates.get(candidate_id)
            if not candidate or candidate.get("status") != "prepared":
                continue
            candidate_result = _qualify_one(run_dir, family, candidate_id, candidate, task_path, task)
            candidate["qualification"] = candidate_result
            if candidate_result["status"] == "qualified":
                qualified_ids.append(candidate_id)
            else:
                candidate["outcome"] = "failed"
        if len(qualified_ids) == 1:
            record["status"] = "no_qualified_candidate"
            record["timing_status"] = "not_run"
            record["qualified_candidates"] = qualified_ids
        else:
            argv = _kda_argv(task_path, Path(record["workspace"]),
                             ["evaluate", "--candidates", *qualified_ids, "--incumbent", "baseline"])
            eval_record = _record_command(run_dir, f"evaluate-{family}", argv, KDA_ROOT,
                                          env={**os.environ, "OPENBLAS_NUM_THREADS": "2", "OMP_NUM_THREADS": "2"},
                                          timeout=1800)
            record["evaluation"] = eval_record
            record["qualified_candidates"] = qualified_ids
            if eval_record["returncode"] == 0 and eval_record.get("json_status") == "ok":
                record["status"] = "evaluated"
                record["timing_status"] = "complete"
            else:
                record["status"] = "evaluation_failed"
                record["timing_status"] = "failed"
        write_json(state_path, state)
    if _terminal_success(state):
        state["status"] = ("completed_no_qualified_candidate"
                            if any(row["status"] == "no_qualified_candidate" for row in state["families"].values())
                            else "qualified_and_evaluated")
    else:
        state["status"] = "failed"
    write_json(state_path, state)
    return state_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare_parser = sub.add_parser("prepare", help="materialize tasks, register sources, and compile on CPU")
    prepare_parser.add_argument("--run-id", required=True)
    prepare_parser.add_argument("--candidate-map", type=Path, required=True)
    qualify_parser = sub.add_parser("qualify", help="controller-qualify candidates, then run KDA timings")
    qualify_parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        run_dir = prepare(args.run_id, args.candidate_map)
        path = run_dir / "run.json"
    else:
        path = qualify(args.run_id)
    final_state = read_json(path)
    success = args.command == "prepare" or _terminal_success(final_state)
    print(json.dumps({"status": "ok" if success else "error", "run": str(path),
                      "run_state": final_state["status"]}, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}), file=sys.stderr)
        raise SystemExit(1)
