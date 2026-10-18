from __future__ import annotations

import json
import math
import sys
import ctypes
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evaluation" / "private"))

from references import (  # noqa: E402
    boolean_epoch,
    boolean_inputs,
    boolean_step,
    energy_inputs,
    energy_guard_inputs,
    gemm_inputs,
    gemm_reference,
    observe_energy,
    within_tolerance,
)
import native_runner  # noqa: E402
import references  # noqa: E402


PUBLIC = ROOT / "evaluation" / "candidate" / "native"
PRIVATE_HOLDOUTS = ROOT / "evaluation" / "private" / "holdouts.json"


class BooleanReferenceTests(unittest.TestCase):
    def test_all_32_local_tuples_are_exercised_in_public_coverage_case(self) -> None:
        case = json.loads((PUBLIC / "bool-transition" / "cases.json").read_text())["cases"][0]
        states, mask, rule = boolean_inputs(case)
        tuples = {(states[i], states[(i - 1) % len(states)], mask[i])
                  for i in range(len(states))}
        self.assertEqual(len(tuples), 32)
        result = boolean_step(states, mask, rule)
        self.assertEqual(len(result), len(states))
        self.assertEqual(set(result), {0, 1, 2, 3})

    def test_updates_are_simultaneous_periodic_and_epoch_local(self) -> None:
        states = [0, 1, 2]
        mask = [0, 1, 0]
        rule = [(i * 3 + 1) % 4 for i in range(32)]
        expected = [rule[(states[i] * 4 + states[(i - 1) % 3]) * 2 + mask[i]]
                    for i in range(3)]
        self.assertEqual(boolean_step(states, mask, rule), expected)
        self.assertEqual(boolean_epoch(states, mask, rule, 0), states)
        other_rule = list(reversed(rule))
        self.assertNotEqual(boolean_step(states, mask, rule), boolean_step(states, mask, other_rule))

    def test_public_boolean_cases_cover_periodic_tails_and_long_epoch(self) -> None:
        cases = json.loads((PUBLIC / "bool-transition" / "cases.json").read_text())["cases"]
        for case in cases:
            states, mask, rule = boolean_inputs(case)
            result = boolean_epoch(states, mask, rule, case["parameters"]["steps"])
            self.assertEqual(len(result), case["parameters"]["n"])
            self.assertTrue(all(value in (0, 1, 2, 3) for value in result))


class ObservableEnergyReferenceTests(unittest.TestCase):
    def test_binary64_reference_uses_represented_inputs_and_detects_weight_updates(self) -> None:
        x = [[[1.0, -2.0]], [[-3.0, 4.0]]]
        weights = [[1.0, 2.0], [-1.0, 0.0]]
        self.assertEqual(observe_energy(x, weights), [[13.0], [85.0]])
        changed = [[1.0, 0.0], [0.0, 1.0]]
        self.assertEqual(observe_energy(x, changed), [[5.0], [25.0]])

    def test_declared_updated_weight_seed_changes_only_the_epoch_weights(self) -> None:
        case = json.loads((PUBLIC / "observable-energy" / "cases.json").read_text())["cases"][1]
        x_first, w_first = energy_inputs(case, weight_seed=case["input"]["w_seed"])
        x_updated, w_updated = energy_inputs(case, weight_seed=case["input"]["w_seed"] + 1)
        self.assertEqual(x_first, x_updated)
        self.assertNotEqual(w_first, w_updated)
        self.assertNotEqual(observe_energy(x_first, w_first), observe_energy(x_updated, w_updated))

    def test_energy_validation_guards_include_zero_cancellation_and_small_scale(self) -> None:
        guards = energy_guard_inputs()
        self.assertEqual(len(guards), 3)
        zeros_x, zeros_w = guards[0]
        self.assertEqual(observe_energy(zeros_x, zeros_w), [[0.0]])
        cancellation_x, cancellation_w = guards[1]
        self.assertEqual(observe_energy(cancellation_x, cancellation_w), [[0.0]])
        small_x, small_w = guards[2]
        small = observe_energy(small_x, small_w)[0][0]
        self.assertGreater(small, 0.0)
        self.assertLess(small, 1e-10)

    def test_public_energy_cases_have_declared_shapes_and_finite_answers(self) -> None:
        cases = json.loads((PUBLIC / "observable-energy" / "cases.json").read_text())["cases"]
        for case in cases:
            x, weights = energy_inputs(case)
            params = case["parameters"]
            self.assertEqual(len(x), params["uses"])
            self.assertTrue(all(len(batch) == params["b"] for batch in x))
            self.assertEqual(len(weights), params["k"])
            self.assertEqual(len(weights[0]), params["m"])
            self.assertTrue(all(math.isfinite(value) for row in x for batch in row for value in batch))
            self.assertTrue(all(math.isfinite(value) for row in weights for value in row))

    def test_flattened_energy_case_requires_capacity_for_all_uses(self) -> None:
        cases = json.loads((PUBLIC / "observable-energy" / "cases.json").read_text())["cases"]
        long_epoch = next(case for case in cases if case["id"] == "large-long-epoch")
        p = long_epoch["parameters"]
        response_elements = p["uses"] * p["b"] * p["m"]
        self.assertEqual(response_elements, 524288)

    def test_tolerance_rejects_non_finite_and_wrong_values(self) -> None:
        self.assertTrue(within_tolerance([1.0], [1.0 + 1e-5], absolute=2e-4, relative=5e-5))
        self.assertFalse(within_tolerance([float("nan")], [1.0], absolute=2e-4, relative=5e-5))
        self.assertFalse(within_tolerance([1.1], [1.0], absolute=2e-4, relative=5e-5))


class DenseGemmReferenceTests(unittest.TestCase):
    def test_binary64_gemm_honors_alpha_beta_and_row_major_dimensions(self) -> None:
        actual = gemm_reference(
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
            [2.0, -1.0, 0.5, 3.0],
            2, 2, 2, 0.75, 0.25,
        )
        self.assertEqual(actual, [14.75, 16.25, 32.375, 38.25])

    def test_public_dense_cases_are_finite_and_preserve_full_output(self) -> None:
        cases = json.loads((PUBLIC / "dense-gemm" / "cases.json").read_text())["cases"]
        for case in cases:
            a, b, c = gemm_inputs(case)
            p = case["parameters"]
            self.assertEqual(len(a), p["m"] * p["k"])
            self.assertEqual(len(b), p["k"] * p["n"])
            self.assertEqual(len(c), p["m"] * p["n"])
            self.assertTrue(all(math.isfinite(value) for value in a + b + c))


class EvaluationBoundaryTests(unittest.TestCase):
    def test_evaluator_holdouts_are_separate_from_candidate_native_tree(self) -> None:
        holdouts = json.loads(PRIVATE_HOLDOUTS.read_text())
        public_ids = {
            family: {case["id"] for case in json.loads((PUBLIC / path / "cases.json").read_text())["cases"]}
            for family, path in (
                ("bool_transition", "bool-transition"),
                ("observable_energy", "observable-energy"),
                ("dense_gemm", "dense-gemm"),
            )
        }
        for family, cases in holdouts.items():
            if isinstance(cases, list):
                self.assertTrue({case["id"] for case in cases}.isdisjoint(public_ids[family]))
        candidate_files = {path.resolve() for path in (ROOT / "evaluation" / "candidate").rglob("*") if path.is_file()}
        self.assertNotIn(PRIVATE_HOLDOUTS.resolve(), candidate_files)
        self.assertNotIn((ROOT / "evaluation" / "private" / "references.py").resolve(), candidate_files)


class NativeRunnerContractTests(unittest.TestCase):
    class SymbolLibrary:
        def __init__(self, symbols: dict[str, object]) -> None:
            self.symbols = symbols
            self.lookups: list[str] = []

        def __getattr__(self, name: str):
            self.lookups.append(name)
            if name in self.symbols:
                return self.symbols[name]
            raise AttributeError(name)

    class FakeCuda:
        def __init__(self) -> None:
            self.memory = {}
            self.next_pointer = 64
            self.stream = ctypes.c_void_p(1)
            self.blas = ctypes.c_void_p(2)

        def alloc(self, size: int):
            pointer = ctypes.c_void_p(self.next_pointer)
            self.next_pointer += max(size, 1) + 16
            return pointer

        def upload(self, pointer, array) -> None:
            import numpy as np
            self.memory[pointer.value] = np.array(array, copy=True, order="C")

        def download(self, pointer, shape, dtype):
            import numpy as np
            return np.array(self.memory[pointer.value], dtype=dtype, copy=True).reshape(shape)

        def synchronize(self) -> None:
            pass

        def synchronize_device(self) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, _kind, _value, _traceback):
            return None

    def test_cublas_versioned_symbols_do_not_evaluate_absent_legacy_fallbacks(self) -> None:
        for versioned, legacy in (("cublasCreate_v2", "cublasCreate"),
                                  ("cublasDestroy_v2", "cublasDestroy")):
            with self.subTest(symbol=versioned):
                symbol = object()
                library = self.SymbolLibrary({versioned: symbol})
                self.assertIs(native_runner._versioned_symbol(library, versioned, legacy), symbol)
                self.assertEqual(library.lookups, [versioned])

    def test_cublas_legacy_symbol_is_looked_up_only_when_versioned_symbol_is_absent(self) -> None:
        symbol = object()
        library = self.SymbolLibrary({"cublasCreate": symbol})
        self.assertIs(native_runner._versioned_symbol(
            library, "cublasCreate_v2", "cublasCreate"), symbol)
        self.assertEqual(library.lookups, ["cublasCreate_v2", "cublasCreate"])

    def test_updated_weights_are_uploaded_between_same_process_calls(self) -> None:
        import numpy as np

        cuda = self.FakeCuda()
        seen_weights = []

        def candidate(x_ptr, w_ptr, b, k, m, uses, out_ptr, _stream, _blas):
            x = cuda.memory[x_ptr.value].reshape(uses * b, k).astype(np.float64)
            weights = cuda.memory[w_ptr.value].reshape(k, m).astype(np.float64)
            values = np.sum((x @ weights) ** 2, axis=1).astype(np.float32)
            cuda.memory[out_ptr.value] = values
            seen_weights.append(cuda.memory[w_ptr.value].copy())
            return 0

        case = {
            "input": {"x_seed": 17, "w_seed": 23},
            "parameters": {"b": 1, "k": 8, "m": 16, "uses": 2},
        }
        self.assertTrue(native_runner._run_energy_updated(cuda, candidate, case, references, 23, 29))
        self.assertEqual(len(seen_weights), 2)
        self.assertFalse(np.array_equal(seen_weights[0], seen_weights[1]))

    def test_output_poison_rejects_stale_or_unwritten_results(self) -> None:
        import numpy as np

        cuda = self.FakeCuda()
        output, count = cuda.alloc(4), cuda.alloc(4)
        native_runner._poison_bool_outputs(cuda, output, count, 4)
        self.assertFalse(np.array_equal(cuda.download(output, (4,), "uint8"), [0, 1, 2, 3]))
        self.assertNotEqual(int(cuda.download(count, (1,), "uint32")[0]), 2)
        energy = cuda.alloc(8)
        native_runner._poison_float_output(cuda, energy, 2)
        self.assertFalse(native_runner._check_float(
            cuda.download(energy, (2,), "float32"), [1.0, 2.0], 2e-4, 5e-5))

    def test_benchmark_rejects_compute_once_then_noop(self) -> None:
        import numpy as np

        cuda = self.FakeCuda()
        calls = 0

        def candidate(x_ptr, w_ptr, b, k, m, uses, out_ptr, _stream, _blas):
            nonlocal calls
            calls += 1
            if calls == 1:
                x = cuda.memory[x_ptr.value].reshape(uses * b, k).astype(np.float64)
                weights = cuda.memory[w_ptr.value].reshape(k, m).astype(np.float64)
                value = np.sum((x @ weights) ** 2, axis=1).astype(np.float32)
                cuda.memory[out_ptr.value] = value
            return 0

        case = {
            "id": "mock-energy",
            "input": {"x_seed": 17, "w_seed": 23},
            "parameters": {"b": 1, "k": 8, "m": 16, "uses": 2},
        }
        request = {
            "candidate": {},
            "case": case,
            "timing": {"warmup": 1, "repetitions": 1, "scope": "test",
                       "metric": "latency", "unit": "us"},
        }
        args = SimpleNamespace(references="unused", cuda_lib_dir="unused",
                               cublas_lib_dir="unused")
        with patch.object(native_runner, "Cuda", return_value=cuda), \
                patch.object(native_runner, "_references", return_value=references), \
                patch.object(native_runner, "_load_candidate", return_value=object()), \
                patch.object(native_runner, "_load_family_api", return_value=candidate):
            with self.assertRaisesRegex(RuntimeError, "repeated benchmark calls"):
                native_runner._benchmark(request, "observable-energy", args)
        self.assertEqual(calls, 2)

    def test_dense_runner_restores_initial_c_before_each_sample(self) -> None:
        import numpy as np

        cuda = self.FakeCuda()
        seen_c = []

        def candidate(a_ptr, b_ptr, c_ptr, m, n, k, alpha, beta, _stream, _blas):
            a = cuda.memory[a_ptr.value].reshape(m, k).astype(np.float64)
            b = cuda.memory[b_ptr.value].reshape(k, n).astype(np.float64)
            c = cuda.memory[c_ptr.value].reshape(m, n).astype(np.float64)
            seen_c.append(c.copy())
            cuda.memory[c_ptr.value] = (alpha * (a @ b) + beta * c).astype(np.float32)
            return 0

        case = {
            "input": {"a_seed": 31, "b_seed": 37, "c_seed": 41},
            "parameters": {"m": 2, "n": 3, "k": 4, "alpha": 0.75, "beta": 0.25},
        }
        passed, samples = native_runner._run_gemm(cuda, candidate, case, references,
                                                  warmup=1, repetitions=2)
        self.assertTrue(passed)
        self.assertEqual(len(samples), 2)
        self.assertEqual(len(seen_c), 3)
        self.assertTrue(all(np.array_equal(seen_c[0], value) for value in seen_c[1:]))


if __name__ == "__main__":
    unittest.main()
