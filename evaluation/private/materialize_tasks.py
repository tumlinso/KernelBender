"""Generate host-bound KDA v1 manifests from the reviewed pilot contracts.

The generated files belong in a private evaluator workspace. Host/controller
paths are supplied at materialization time and never enter candidate bundles.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]
NATIVE = ROOT / "evaluation" / "candidate" / "native"
PRIVATE = ROOT / "evaluation" / "private"

FAMILIES = {
    "bool-transition": {
        "task_id": "kb-native-bool-transition-v1",
        "metric": "full_epoch_latency",
        "scope": "wall-clock time for one resident-input kb_run call through full-device completion; includes candidate allocations, all transitions, aggregate output, and completion synchronization; host input setup and copies are excluded",
        "absolute": 0.0,
        "relative": 0.0,
    },
    "observable-energy": {
        "task_id": "kb-native-observable-energy-v1",
        "metric": "full_epoch_latency",
        "scope": "wall-clock time for one resident-input kb_run call through full-device completion; includes candidate allocations, all U uses, preparation, output, and completion synchronization; host input setup and copies are excluded",
        "absolute": 2e-4,
        "relative": 5e-5,
    },
    "dense-gemm": {
        "task_id": "kb-native-dense-gemm-control-v1",
        "metric": "operator_latency",
        "scope": "wall-clock time for one resident-input kb_run call through full-device completion; includes completion synchronization; C is restored and synchronized immediately before timing, and restore time is excluded",
        "absolute": 2e-5,
        "relative": 5e-5,
    },
}


def _command(python: str, runner: Path, operation: str, family: str,
             references: Path, holdouts: Path, cuda_lib_dir: Path,
             cublas_lib_dir: Path, nvcc: Path) -> list[str]:
    return [python, str(runner), operation, "--family", family,
            "--references", str(references), "--holdouts", str(holdouts),
            "--cuda-lib-dir", str(cuda_lib_dir), "--cublas-lib-dir", str(cublas_lib_dir),
            "--nvcc", str(nvcc),
            "{request}", "{result}"]


def materialize(family: str, output: Path, *, site_config: Path, kda_root: Path,
                nvcc: Path, cuda_lib_dir: Path, cublas_lib_dir: Path,
                controller_entry: Path, runtime_identity: Path,
                cuda_controller_script: Path) -> Path:
    if family not in FAMILIES:
        raise ValueError(f"unknown family: {family}")
    for path in (site_config, kda_root / "kda_experiments" / "controller_launcher.py",
                 nvcc, cuda_lib_dir / "libcudart.so", cublas_lib_dir / "libcublas.so",
                 controller_entry, runtime_identity, cuda_controller_script):
        if not path.exists():
            raise FileNotFoundError(path)
    native = NATIVE / family
    cases = json.loads((native / "cases.json").read_text(encoding="utf-8"))["cases"]
    details = FAMILIES[family]
    python = sys.executable
    runner = (PRIVATE / "native_runner.py").resolve()
    references = (PRIVATE / "references.py").resolve()
    holdouts = (PRIVATE / "holdouts.json").resolve()
    baseline = (native / "baseline" / "kernel.cu").resolve()
    api = (native / "candidate_api.h").resolve()
    kda_root = kda_root.resolve(strict=True)
    site_config = site_config.resolve(strict=True)
    nvcc = nvcc.resolve(strict=True)
    cuda_lib_dir = cuda_lib_dir.resolve(strict=True)
    cublas_lib_dir = cublas_lib_dir.resolve(strict=True)
    controller_entry = controller_entry.resolve(strict=True)
    runtime_identity = runtime_identity.resolve(strict=True)
    cuda_controller_script = cuda_controller_script.resolve(strict=True)
    launcher = (kda_root / "kda_experiments" / "controller_launcher.py").resolve(strict=True)

    runner_command = lambda operation: _command(python, runner, operation, family,
                                                 references, holdouts, cuda_lib_dir,
                                                 cublas_lib_dir, nvcc)
    task = {
        "schema_version": 1,
        "task_id": details["task_id"],
        "cases": cases,
        "commands": {
            "build": {"argv": runner_command("build"), "cpu_only": True, "timeout_seconds": 180},
            "validate": {"argv": runner_command("validate"), "timeout_seconds": 180},
            "benchmark": {"argv": runner_command("benchmark"), "timeout_seconds": 180},
        },
        "trusted_inputs": [
            {"id": "native_runner", "path": str(runner), "role": "harness"},
            {"id": "independent_references", "path": str(references), "role": "reference"},
            {"id": "private_holdouts", "path": str(holdouts), "role": "reference"},
            {"id": "public_candidate_api", "path": str(api), "role": "other"},
            {"id": "corrected_native_baseline", "path": str(baseline), "role": "other"},
            {"id": "site_execution_policy", "path": str(site_config), "role": "toolchain"},
            {"id": "kda_controller_launcher", "path": str(launcher), "role": "harness"},
            {"id": "site_controller_entry", "path": str(controller_entry), "role": "harness"},
            {"id": "site_runtime_identity", "path": str(runtime_identity), "role": "toolchain"},
            {"id": "cuda_controller_script", "path": str(cuda_controller_script), "role": "harness"},
        ],
        "numerical_requirements": {
            "reference": "independent host float64 operation over the represented FP32 inputs; Boolean transition uses exact integer semantics",
            "absolute_tolerance": details["absolute"],
            "relative_tolerance": details["relative"],
            "reordering": "permitted only when every public and evaluator-only validation case passes the fixed tolerance",
        },
        "probe": {"argv": runner_command("probe"), "timeout_seconds": 30},
        "timing": {
            "metric": details["metric"],
            "unit": "microsecond",
            "direction": "minimize",
            "warmup": 2,
            "repetitions": 3,
            "rounds": 2,
            "confirmation_rounds": 2,
            "seed": 1701,
            "scope": details["scope"],
        },
        "promotion": {"min_improvement": 0.02, "max_regression": 0.10,
                      "confidence": 0.95, "bootstrap_samples": 1000},
        "target": {"kind": "cuda", "architecture": "sm_70", "compiler_target": "sm_70"},
        "toolchain": {"compiler_target_probe_argv": [str(nvcc), "--list-gpu-code"]},
        "execution": {
            "mode": "launcher",
            "launcher_argv": [python, "-m", "kda_experiments.controller_launcher",
                              "--config", str(site_config), "--request", "{request}",
                              "--result", "{result}"],
        },
        "budgets": {"max_candidates": 8, "max_build_jobs": 1, "max_seconds": 900},
    }
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "task.json"
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite an existing KDA task: {destination}")
    destination.write_text(json.dumps(task, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=sorted(FAMILIES))
    parser.add_argument("--output", type=Path, required=True, help="private KDA task directory")
    parser.add_argument("--site-config", type=Path, required=True, help="site-owned controller launcher JSON")
    parser.add_argument("--kda-root", type=Path, required=True)
    parser.add_argument("--nvcc", type=Path, required=True, help="explicit CUDA 12.9 compiler")
    parser.add_argument("--cuda-lib-dir", type=Path, required=True, help="CUDA 12.9 lib64 directory")
    parser.add_argument("--cublas-lib-dir", type=Path, required=True, help="CUDA 12.9 cuBLAS library directory")
    parser.add_argument("--controller-entry", type=Path, required=True)
    parser.add_argument("--runtime-identity", type=Path, required=True)
    parser.add_argument("--cuda-controller-script", type=Path, required=True)
    args = parser.parse_args()
    destination = materialize(args.family, args.output.resolve(), site_config=args.site_config,
                              kda_root=args.kda_root, nvcc=args.nvcc, cuda_lib_dir=args.cuda_lib_dir,
                              cublas_lib_dir=args.cublas_lib_dir,
                              controller_entry=args.controller_entry,
                              runtime_identity=args.runtime_identity,
                              cuda_controller_script=args.cuda_controller_script)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
