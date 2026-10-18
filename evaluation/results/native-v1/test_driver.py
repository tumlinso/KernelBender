"""CPU-only contract tests for the native pilot orchestration driver."""

from __future__ import annotations

import json
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import driver


class DriverContractTests(unittest.TestCase):
    def _negative_terminal_state(self) -> dict:
        return {"status": "qualifying", "families": {
            family: {
                "status": "no_qualified_candidate", "timing_status": "not_run",
                "qualified_candidates": ["baseline"],
                "candidates": {
                    "baseline": {"status": "prepared", "qualification": {"status": "qualified"}},
                    "candidate-a": {"status": "qualification_failed", "outcome": "failed",
                                    "qualification": {"status": "qualification_failed"}},
                    "candidate-b": {"status": "no_candidate", "outcome": "no_candidate"},
                },
            }
            for family in driver.FAMILIES
        }}

    def _candidate_map(self, root: Path) -> dict:
        rows = {}
        for family in driver.FAMILIES:
            rows[family] = {}
            for arm in driver.ARMS:
                folder = root / family / arm
                folder.mkdir(parents=True)
                receipt = folder / "receipt.json"
                commands = folder / "commands.jsonl"
                receipt.write_text("{}\n", encoding="utf-8")
                commands.write_text("{}\n", encoding="utf-8")
                rows[family][arm] = {
                    "trial_id": f"{family}-{arm}", "outcome": "no_candidate",
                    "build_attempts": 0, "candidate_source": None,
                    "attempt_records": [
                        {"kind": "receipt", "path": str(receipt), "sha256": driver.sha256_file(receipt)},
                        {"kind": "commands", "path": str(commands), "sha256": driver.sha256_file(commands)},
                    ],
                }
        return {
            "schema_version": 1, "run_id": "contract-test",
            "trial_policy_sha256": driver.sha256_file(driver.TRIAL_POLICY),
            "source_manifest_sha256": driver.sha256_file(driver.SOURCE_MANIFEST),
            "agent_policy_sha256": driver.sha256_file(driver.AGENT_POLICY),
            "input_manifests_sha256": driver.sha256_file(driver.INPUT_MANIFESTS),
            "families": rows,
        }

    def _completed_run_fixture(self, runs_root: Path) -> tuple[str, Path, Path, Path, Path]:
        run_id = "completed-fixture"
        run_dir = runs_root / run_id
        run_dir.mkdir(parents=True)
        external = runs_root / "external-inputs"
        external.mkdir()
        state = self._negative_terminal_state()
        state.update(schema_version=1, run_id=run_id, status="qualified_and_evaluated")
        for key in driver.PINNED_STATE_FILES:
            if key == "driver":
                path = Path(driver.__file__).resolve()
            else:
                path = external / f"{key}.json"
                path.write_text(f"fixture:{key}\n", encoding="utf-8")
            state[key] = str(path)
            state[f"{key}_sha256"] = driver.sha256_file(path)
        state["families"] = {}

        def write_file(path: Path, contents: str) -> tuple[str, str]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
            return str(path), driver.sha256_file(path)

        external_source = external / "trusted-source.json"
        external_source.write_text("trusted fixture source\n", encoding="utf-8")
        for family in driver.FAMILIES:
            workspace = run_dir / "work" / family
            workspace.mkdir(parents=True)
            (workspace / "candidates.jsonl").write_text('{"record_type":"evaluation"}\n', encoding="utf-8")
            (workspace / "benchmark.csv").write_text("candidate,round,latency_ms\nbaseline,0,1.0\n", encoding="utf-8")
            task_path = run_dir / "tasks" / family / "task.json"
            task_path.parent.mkdir(parents=True)
            task_path.write_text(json.dumps({"trusted_inputs": [
                {"id": "fixture-source", "path": str(external_source), "role": "other"}]}),
                encoding="utf-8")
            task_hash = driver.sha256_file(task_path)
            summary_path = external / f"{family}-kda-summary.json"
            summary_path.write_text(json.dumps({
                "status": "complete", "run_id": f"kda-{family}",
                "validation": {"baseline": {"status": "pass"},
                               "candidate-a": {"status": "pass"}},
                "benchmark_failures": {}, "confirmation": None,
            }), encoding="utf-8")
            family_state = {
                "status": "evaluated", "timing_status": "complete",
                "task": str(task_path), "task_sha256": task_hash,
                "qualified_candidates": ["baseline", "candidate-a"],
                "candidates": {},
            }
            eval_stdout, eval_stdout_hash = write_file(workspace / "kda.stdout", "kda completed\n")
            eval_stderr, eval_stderr_hash = write_file(workspace / "kda.stderr", "\n")
            family_state["evaluation"] = {
                "returncode": 0, "json_status": "ok",
                "stdout_path": eval_stdout, "stdout_sha256": eval_stdout_hash,
                "stderr_path": eval_stderr, "stderr_sha256": eval_stderr_hash,
                "summary_path_sha256": driver.sha256_file(summary_path),
                "json": {"engine_status": "complete", "run_id": f"kda-{family}",
                         "summary_path": str(summary_path)},
            }
            for candidate_id in ("baseline", "candidate-a"):
                source_dir = workspace / "candidates" / candidate_id
                source_path, source_hash = write_file(source_dir / "kernel.cu", f"source {candidate_id}\n")
                binary_path, binary_hash = write_file(workspace / "build" / f"{candidate_id}.so", "binary\n")
                source_identity = [{"path": "kernel.cu", "sha256": source_hash}]
                sanitizers = []
                for tool in ("memcheck", "racecheck"):
                    evidence_dir = run_dir / "qualification" / family / candidate_id / tool
                    wrapper_out, wrapper_out_hash = write_file(evidence_dir / "wrapper.stdout", "controller ok\n")
                    wrapper_err, wrapper_err_hash = write_file(evidence_dir / "wrapper.stderr", "\n")
                    actual_out, actual_out_hash = write_file(
                        external / f"{family}-{candidate_id}-{tool}-controller.stdout", "sanitizer summary\n")
                    actual_err, actual_err_hash = write_file(evidence_dir / "controller.stderr", "\n")
                    raw_log, raw_hash = write_file(
                        external / f"{family}-{candidate_id}-{tool}-raw.log", "zero errors\n")
                    summary_txt, summary_hash = write_file(evidence_dir / "summary.txt", "status: ok\n")
                    summary_json = Path(summary_txt).with_suffix(".json")
                    _, summary_json_hash = write_file(summary_json, '{"exit_status": 0}\n')
                    validator_path, validator_hash = write_file(
                        external / f"{family}-{candidate_id}-{tool}-validation-result.json", '{"status":"ok"}\n')
                    sanitizers.append({
                        "tool": tool, "passed": True,
                        "controller": {
                            "returncode": 0, "json_status": "succeeded",
                            "stdout_path": wrapper_out, "stdout_sha256": wrapper_out_hash,
                            "stderr_path": wrapper_err, "stderr_sha256": wrapper_err_hash,
                        },
                        "sanitizer": {
                            "passed": True,
                            "raw_log_path": raw_log, "raw_log_sha256": raw_hash,
                            "summary_path": summary_txt, "summary_sha256": summary_hash,
                            "summary_json_path": str(summary_json), "summary_json_sha256": summary_json_hash,
                            "target_exit_status": 0,
                            "controller_stdout_path": actual_out,
                            "controller_stdout_sha256": actual_out_hash,
                            "controller_stderr_path": actual_err,
                            "controller_stderr_sha256": actual_err_hash,
                        },
                        "validation_result_path": validator_path,
                        "validation_result_sha256": validator_hash,
                    })
                family_state["candidates"][candidate_id] = {
                    "status": "prepared", "record": {
                        "snapshot_dir": str(source_dir),
                        "source_manifest": [{"path": "kernel.cu", "sha256": source_hash}],
                    },
                    "qualification": {
                        "status": "qualified", "candidate_id": candidate_id,
                        "source_identity_before": source_identity,
                        "source_identity_after": source_identity,
                        "binary_sha256_before": binary_hash, "binary_sha256_after": binary_hash,
                        "artifacts": [{"path": binary_path, "sha256": binary_hash}],
                        "sanitizers": sanitizers,
                    },
                }
            family_state["candidates"]["candidate-b"] = {
                "status": "no_candidate", "outcome": "no_candidate",
            }
            state["families"][family] = family_state
        manifest_hash = driver._record_completion_evidence(run_dir, state)
        state["completion_evidence_sha256"] = manifest_hash
        state_path = run_dir / "run.json"
        state_path.write_text(json.dumps(state, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        raw_log = external / f"{driver.FAMILIES[0]}-baseline-memcheck-raw.log"
        return (run_id, run_dir, state_path,
                run_dir / "work" / driver.FAMILIES[0] / "build" / "baseline.so", raw_log)

    def test_candidate_map_requires_all_families_arms_and_trial_evidence(self) -> None:
        policy = driver.read_json(driver.TRIAL_POLICY)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = self._candidate_map(root)
            path = root / "map.json"
            path.write_text(json.dumps(valid), encoding="utf-8")
            self.assertEqual(driver._validate_candidate_map(path, "contract-test", policy)["run_id"],
                             "contract-test")

            missing_arm = json.loads(path.read_text())
            del missing_arm["families"][driver.FAMILIES[0]]["A"]["attempt_records"][0]
            path.write_text(json.dumps(missing_arm), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "command log and trial receipt"):
                driver._validate_candidate_map(path, "contract-test", policy)

            too_many = self._candidate_map(root / "other")
            too_many["families"][driver.FAMILIES[1]]["B"]["build_attempts"] = 3
            path.write_text(json.dumps(too_many), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen limit"):
                driver._validate_candidate_map(path, "contract-test", policy)

    def test_native_runner_exit_zero_does_not_override_json_error(self) -> None:
        task = {"cases": [{"id": "case-1", "input": {"seed": 1}, "parameters": {"n": 3}}]}
        case = task["cases"][0]
        row = {**driver._workload_descriptor(case), "case_id": case["id"], "status": "pass"}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "result.json"
            path.write_text(json.dumps({"schema_version": 1, "request_id": "rid", "status": "error",
                                        "cases": [row], "private_checks": {"status": "pass"}}),
                            encoding="utf-8")
            self.assertEqual(driver._validate_runner_json(path, task, "rid")["status"], "failed")

            valid = json.loads(path.read_text())
            valid["status"] = "ok"
            valid["private_checks"]["status"] = "fail"
            path.write_text(json.dumps(valid), encoding="utf-8")
            self.assertEqual(driver._validate_runner_json(path, task, "rid")["status"], "failed")

    def test_memcheck_summary_requires_zero_errors_and_target_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw.log"
            summary = root / "summary.txt"
            stdout = root / "controller.stdout"
            raw.write_text("========= ERROR SUMMARY: 0 errors\n", encoding="utf-8")
            summary.write_text("status: ok\n", encoding="utf-8")
            summary_json = summary.with_suffix(".json")
            summary_json.write_text('{"exit_status": 0}\n', encoding="utf-8")
            stdout.write_text(f"Compute Sanitizer summary: {summary}\n- raw log: {raw}\n", encoding="utf-8")
            record = {"json": {"stdout_path": str(stdout), "stderr_path": None, "ok": True,
                                "status": "succeeded"}}
            result = driver._parse_sanitizer_artifacts(record, "memcheck")
            self.assertTrue(result["passed"])
            self.assertEqual(result["target_exit_status"], 0)

            summary_json.write_text('{"exit_status": 86}\n', encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "memcheck")["passed"])

            summary_json.write_text("{}\n", encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "memcheck")["passed"])

            summary_json.write_text('{"exit_status": false}\n', encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "memcheck")["passed"])

            summary_json.unlink()
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "memcheck")["passed"])

            raw.write_text("========= ERROR SUMMARY: 2 errors\n", encoding="utf-8")
            summary_json.write_text('{"exit_status": 0}\n', encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "memcheck")["passed"])

    def test_racecheck_actual_summary_requires_zero_hazards_errors_and_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw.log"
            summary = root / "summary.txt"
            stdout = root / "controller.stdout"
            summary.write_text("status: ok\n", encoding="utf-8")
            summary.with_suffix(".json").write_text('{"exit_status": 0}\n', encoding="utf-8")
            stdout.write_text(f"Compute Sanitizer summary: {summary}\n- raw log: {raw}\n", encoding="utf-8")
            record = {"json": {"stdout_path": str(stdout), "stderr_path": None, "ok": True,
                                "status": "succeeded"}}

            # Exact RACECHECK SUMMARY line format observed in the existing KDA logs.
            raw.write_text("========= COMPUTE-SANITIZER\n"
                           "========= RACECHECK SUMMARY: 0 hazards displayed (0 errors, 0 warnings)\n",
                           encoding="utf-8")
            result = driver._parse_sanitizer_artifacts(record, "racecheck")
            self.assertTrue(result["passed"])
            self.assertEqual(result["sanitizer_summaries"],
                             [{"hazards": 0, "errors": 0, "warnings": 0}])

            raw.write_text("========= Target application returned an error\n"
                           "========= RACECHECK SUMMARY: 24 hazards displayed (24 errors, 0 warnings)\n",
                           encoding="utf-8")
            result = driver._parse_sanitizer_artifacts(record, "racecheck")
            self.assertFalse(result["passed"])
            self.assertEqual(result["sanitizer_summaries"],
                             [{"hazards": 24, "errors": 24, "warnings": 0}])

            raw.write_text("========= RACECHECK SUMMARY: 0 hazards displayed (0 errors, 1 warning)\n",
                           encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "racecheck")["passed"])

            raw.write_text("========= ERROR SUMMARY: 0 errors\n", encoding="utf-8")
            self.assertFalse(driver._parse_sanitizer_artifacts(record, "racecheck")["passed"])

    def test_qualify_reuses_completed_run_without_gpu_and_rejects_mutated_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_id, run_dir, state_path, binary, _ = self._completed_run_fixture(root)
            original_state = state_path.read_bytes()
            external_ids = {item["id"] for item in driver.read_json(
                run_dir / driver.COMPLETION_EVIDENCE_NAME)["external_inputs"]}
            self.assertIn(f"kda:{driver.FAMILIES[0]}:summary", external_ids)
            self.assertIn(f"sanitizer:{driver.FAMILIES[0]}:baseline:0:raw_log_path", external_ids)
            self.assertIn(f"validator:{driver.FAMILIES[0]}:baseline:0", external_ids)
            with patch.object(driver, "RUNS_ROOT", root), \
                 patch.object(driver, "_qualify_one", side_effect=AssertionError("GPU qualification reran")):
                self.assertEqual(driver.qualify(run_id), state_path)
            self.assertEqual(state_path.read_bytes(), original_state)

            binary.write_text("mutated binary\n", encoding="utf-8")
            with patch.object(driver, "RUNS_ROOT", root), \
                 patch.object(driver, "_qualify_one", side_effect=AssertionError("GPU qualification reran")):
                with self.assertRaisesRegex(ValueError, "hash changed|evidence files changed"):
                    driver.qualify(run_id)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_id, run_dir, _, _, raw_log = self._completed_run_fixture(root)
            raw_log.write_text("mutated sanitizer evidence\n", encoding="utf-8")
            with patch.object(driver, "RUNS_ROOT", root), \
                 patch.object(driver, "_qualify_one", side_effect=AssertionError("GPU qualification reran")):
                with self.assertRaisesRegex(ValueError, "hash changed|evidence files changed"):
                    driver.qualify(run_id)

    def test_controller_receipt_requires_successful_admission_and_capture(self) -> None:
        record = {"returncode": 0, "json_status": "succeeded",
                  "json": {"ok": True, "status": "succeeded", "evidence_id": "e:test"}}
        self.assertTrue(driver._controller_succeeded(record))
        record["json"]["ok"] = False
        self.assertFalse(driver._controller_succeeded(record))
        record["json"]["ok"] = True
        record["json_status"] = "failed"
        self.assertFalse(driver._controller_succeeded(record))

    def test_command_receipt_preserves_timeout_and_exact_argv(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(driver.subprocess, "run", side_effect=driver.subprocess.TimeoutExpired(["tool"], 1)):
                record = driver._record_command(root, "timeout", ["tool", "--flag"], root, timeout=1)
            self.assertIsNone(record["returncode"])
            self.assertEqual(record["argv"], ["tool", "--flag"])
            self.assertIn("TimeoutExpired", Path(record["stderr_path"]).read_text())

    def test_qualify_exit_accepts_rejections_but_fails_baseline_or_evaluation_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "run.json"
            state = self._negative_terminal_state()
            cases = [(state, 0)]

            baseline_failure = json.loads(json.dumps(state))
            baseline_failure["families"][driver.FAMILIES[0]]["status"] = "baseline_qualification_failed"
            baseline_failure["families"][driver.FAMILIES[0]]["candidates"]["baseline"]["qualification"]["status"] = "qualification_failed"
            cases.append((baseline_failure, 1))

            evaluation_failure = json.loads(json.dumps(state))
            family = evaluation_failure["families"][driver.FAMILIES[1]]
            family["status"] = "evaluation_failed"
            family["timing_status"] = "failed"
            family["candidates"]["candidate-a"]["qualification"]["status"] = "qualified"
            family["qualified_candidates"] = ["baseline", "candidate-a"]
            family["evaluation"] = {"returncode": 1, "json_status": "error"}
            cases.append((evaluation_failure, 1))

            for result, expected in cases:
                path.write_text(json.dumps(result), encoding="utf-8")
                with patch.object(driver, "qualify", return_value=path), redirect_stdout(io.StringIO()):
                    self.assertEqual(driver.main(["qualify", "--run-id", "contract-test"]), expected)

    def test_terminal_success_accepts_completed_kda_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = self._negative_terminal_state()
            for family_name, family in state["families"].items():
                run_id = f"run-{family_name}"
                candidate = family["candidates"]["candidate-a"]
                candidate.update(status="prepared", outcome="candidate_ready",
                                 qualification={"status": "qualified"})
                family.update(status="evaluated", timing_status="complete",
                              qualified_candidates=["baseline", "candidate-a"])
                summary = root / f"{family_name}.json"
                summary.write_text(json.dumps({
                    "status": "complete", "run_id": run_id,
                    "validation": {"baseline": {"status": "pass"},
                                   "candidate-a": {"status": "pass"}},
                    "benchmark_failures": {}, "confirmation": None,
                }), encoding="utf-8")
                family["evaluation"] = {
                    "returncode": 0, "json_status": "ok",
                    "json": {"engine_status": "complete", "run_id": run_id,
                             "summary_path": str(summary)},
                }
            self.assertTrue(driver._terminal_success(state))


if __name__ == "__main__":
    unittest.main()
