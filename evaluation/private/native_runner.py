"""Trusted KDA runner for the bounded KernelBender native pilot.

This module is evaluator-only. Candidate code is loaded from its immutable KDA
snapshot and cannot provide references, validation logic, or timing policy.
The runner deliberately requires a real CUDA device for probe/validate/bench;
CPU-only checks exercise references and task contracts without faking results.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
from typing import Any


def _read(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: str | Path, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, target)


def _references(path: str | Path):
    spec = importlib.util.spec_from_file_location("kernelbender_native_references", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load trusted references from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cuda:
    """Small ctypes binding for only the runtime operations used by this pilot."""

    def __init__(self, libdir: str | Path, cublas_libdir: str | Path):
        root = Path(libdir)
        self.runtime = ctypes.CDLL(str(root / "libcudart.so"))
        self.runtime.cudaGetErrorString.restype = ctypes.c_char_p
        self.runtime.cudaMalloc.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_size_t]
        self.runtime.cudaFree.argtypes = [ctypes.c_void_p]
        self.runtime.cudaMemcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
        self.runtime.cudaStreamCreateWithFlags.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint]
        self.runtime.cudaStreamSynchronize.argtypes = [ctypes.c_void_p]
        self.runtime.cudaDeviceSynchronize.argtypes = []
        self.runtime.cudaStreamDestroy.argtypes = [ctypes.c_void_p]
        self.runtime.cudaGetDeviceCount.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.runtime.cudaGetDevice.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.runtime.cudaDeviceGetAttribute.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
        self.runtime.cudaRuntimeGetVersion.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.runtime.cudaDriverGetVersion.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.runtime.cudaGetLastError.restype = ctypes.c_int
        self.runtime.cudaEventCreate.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.runtime.cudaEventRecord.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.runtime.cudaEventSynchronize.argtypes = [ctypes.c_void_p]
        self.runtime.cudaEventElapsedTime.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_void_p, ctypes.c_void_p]
        self.runtime.cudaEventDestroy.argtypes = [ctypes.c_void_p]
        self.cublas = ctypes.CDLL(str(Path(cublas_libdir) / "libcublas.so"))
        self._cublas_create = getattr(self.cublas, "cublasCreate_v2", self.cublas.cublasCreate)
        self._cublas_destroy = getattr(self.cublas, "cublasDestroy_v2", self.cublas.cublasDestroy)
        self._cublas_create.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self._cublas_destroy.argtypes = [ctypes.c_void_p]
        self.stream = ctypes.c_void_p()
        self.check(self.runtime.cudaStreamCreateWithFlags(ctypes.byref(self.stream), 1), "cudaStreamCreateWithFlags")
        self.blas = ctypes.c_void_p()
        self.allocations: list[ctypes.c_void_p] = []
        status = self._cublas_create(ctypes.byref(self.blas))
        if status != 0:
            self.close()
            raise RuntimeError(f"cublasCreate returned status {status}")

    def check(self, status: int, operation: str) -> None:
        if status != 0:
            message = self.runtime.cudaGetErrorString(status)
            detail = message.decode("utf-8", "replace") if message else f"CUDA status {status}"
            raise RuntimeError(f"{operation}: {detail}")

    def alloc(self, size: int) -> ctypes.c_void_p:
        if size <= 0:
            raise ValueError("device allocation size must be positive")
        pointer = ctypes.c_void_p()
        self.check(self.runtime.cudaMalloc(ctypes.byref(pointer), size), "cudaMalloc")
        self.allocations.append(pointer)
        return pointer

    def upload(self, pointer: ctypes.c_void_p, array) -> None:
        import numpy as np

        value = np.ascontiguousarray(array)
        self.check(self.runtime.cudaMemcpy(pointer, ctypes.c_void_p(value.ctypes.data), value.nbytes, 1), "cudaMemcpy H2D")

    def download(self, pointer: ctypes.c_void_p, shape: tuple[int, ...], dtype):
        import numpy as np

        value = np.empty(shape, dtype=dtype)
        self.check(self.runtime.cudaMemcpy(ctypes.c_void_p(value.ctypes.data), pointer, value.nbytes, 2), "cudaMemcpy D2H")
        return value

    def synchronize(self) -> None:
        self.check(self.runtime.cudaStreamSynchronize(self.stream), "cudaStreamSynchronize")

    def synchronize_device(self) -> None:
        self.check(self.runtime.cudaDeviceSynchronize(), "cudaDeviceSynchronize")

    def close(self) -> None:
        if getattr(self, "stream", None) and self.stream.value:
            self.synchronize()
        for pointer in reversed(getattr(self, "allocations", [])):
            if pointer.value:
                self.check(self.runtime.cudaFree(pointer), "cudaFree evaluator buffer")
        self.allocations = []
        if getattr(self, "blas", None) and self.blas.value:
            status = self._cublas_destroy(self.blas)
            self.blas = ctypes.c_void_p()
            if status != 0:
                raise RuntimeError(f"cublasDestroy returned status {status}")
        if getattr(self, "stream", None) and self.stream.value:
            status = self.runtime.cudaStreamDestroy(self.stream)
            self.stream = ctypes.c_void_p()
            self.check(status, "cudaStreamDestroy")

    def __enter__(self):
        return self

    def __exit__(self, _kind, _value, _traceback):
        self.close()


def _gpu_environment(cuda: Cuda, nvcc: str) -> dict[str, Any]:
    count = ctypes.c_int()
    current = ctypes.c_int()
    cuda.check(cuda.runtime.cudaGetDeviceCount(ctypes.byref(count)), "cudaGetDeviceCount")
    cuda.check(cuda.runtime.cudaGetDevice(ctypes.byref(current)), "cudaGetDevice")
    if count.value < 1:
        raise RuntimeError("no CUDA device is visible to the admitted task")
    major, minor = ctypes.c_int(), ctypes.c_int()
    multiprocessors = ctypes.c_int()
    cuda.check(cuda.runtime.cudaDeviceGetAttribute(ctypes.byref(major), 75, current.value), "compute-capability major")
    cuda.check(cuda.runtime.cudaDeviceGetAttribute(ctypes.byref(minor), 76, current.value), "compute-capability minor")
    cuda.check(cuda.runtime.cudaDeviceGetAttribute(ctypes.byref(multiprocessors), 16, current.value), "multiprocessor count")
    driver = ctypes.CDLL("libcuda.so.1")
    driver.cuInit.argtypes = [ctypes.c_uint]
    driver.cuDeviceGet.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    driver.cuDeviceGetName.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    driver.cuDeviceGetUuid_v2.argtypes = [ctypes.c_void_p, ctypes.c_int]
    device = ctypes.c_int()
    for name, status in (("cuInit", driver.cuInit(0)),):
        if status != 0:
            raise RuntimeError(f"{name} returned status {status}")
    status = driver.cuDeviceGet(ctypes.byref(device), current.value)
    if status != 0:
        raise RuntimeError(f"cuDeviceGet returned status {status}")
    name_buffer = ctypes.create_string_buffer(256)
    status = driver.cuDeviceGetName(name_buffer, len(name_buffer), device.value)
    if status != 0:
        raise RuntimeError(f"cuDeviceGetName returned status {status}")
    uuid_bytes = (ctypes.c_ubyte * 16)()
    status = driver.cuDeviceGetUuid_v2(ctypes.byref(uuid_bytes), device.value)
    if status != 0:
        raise RuntimeError(f"cuDeviceGetUuid_v2 returned status {status}")
    runtime_version, driver_version = ctypes.c_int(), ctypes.c_int()
    cuda.check(cuda.runtime.cudaRuntimeGetVersion(ctypes.byref(runtime_version)), "cudaRuntimeGetVersion")
    cuda.check(cuda.runtime.cudaDriverGetVersion(ctypes.byref(driver_version)), "cudaDriverGetVersion")
    nvcc_result = subprocess.run([nvcc, "--version"], check=True, capture_output=True, text=True)
    import numpy as np

    uuid = "GPU-" + bytes(uuid_bytes).hex()
    return {
        "kind": "cuda",
        "architecture": f"sm_{major.value}{minor.value}",
        "compute_capability": f"{major.value}.{minor.value}",
        "device_uuid": uuid,
        "device": {"index": current.value, "uuid": uuid, "name": name_buffer.value.decode("utf-8", "replace")},
        "multiprocessor_count": multiprocessors.value,
        "driver_version": str(driver_version.value),
        "runtime_version": str(runtime_version.value),
        "tools": {"python": sys.version.split()[0], "numpy": np.__version__,
                  "numpy_threads": {name: os.environ.get(name) for name in
                                    ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
                  "nvcc": nvcc_result.stdout.strip().splitlines()[-1]},
    }


def _load_candidate(request: dict[str, Any]):
    artifacts = request["candidate"]["build"]["artifacts"]
    root = Path(request["candidate"]["build"]["directory"])
    libraries = [root / item["path"] for item in artifacts if str(item["path"]).endswith(".so")]
    if len(libraries) != 1:
        raise RuntimeError("candidate build must provide exactly one shared library")
    return ctypes.CDLL(str(libraries[0]))


def _load_family_api(library, family: str):
    function = library.kb_run
    pointer = ctypes.c_void_p
    if family == "bool-transition":
        function.argtypes = [pointer, pointer, pointer, ctypes.c_int, ctypes.c_int, pointer, pointer, pointer]
    elif family == "observable-energy":
        function.argtypes = [pointer, pointer, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, pointer, pointer, pointer]
    elif family == "dense-gemm":
        function.argtypes = [pointer, pointer, pointer, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                             ctypes.c_float, ctypes.c_float, pointer, pointer]
    else:
        raise ValueError(f"unknown native task family {family!r}")
    function.restype = ctypes.c_int
    return function


def _call_checked(function, args, family: str) -> None:
    status = function(*args)
    if status != 0:
        raise RuntimeError(f"{family} candidate kb_run returned {status}")


def _float32(value):
    import numpy as np

    return np.ascontiguousarray(value, dtype=np.float32)


def _check_float(actual, expected, absolute: float, relative: float) -> bool:
    import numpy as np

    actual = np.asarray(actual, dtype=np.float64)
    expected = np.asarray(expected, dtype=np.float64)
    return bool(actual.shape == expected.shape and np.isfinite(actual).all() and np.isfinite(expected).all()
                and (np.abs(actual - expected) <= absolute + relative * np.abs(expected)).all())


def _energy_reference_numpy(x, weights):
    import numpy as np

    x64 = np.asarray(x, dtype=np.float32).astype(np.float64)
    w64 = np.asarray(weights, dtype=np.float32).astype(np.float64)
    response = x64.reshape((-1, w64.shape[0])) @ w64
    return np.sum(response * response, axis=1, dtype=np.float64)


def _gemm_reference_numpy(a, b, c, alpha: float, beta: float):
    import numpy as np

    a64 = np.asarray(a, dtype=np.float32).astype(np.float64)
    b64 = np.asarray(b, dtype=np.float32).astype(np.float64)
    c64 = np.asarray(c, dtype=np.float32).astype(np.float64)
    return alpha * (a64 @ b64) + beta * c64


def _new_bool_buffers(cuda: Cuda, states, mask, rule):
    import numpy as np

    state, mask_array, rule_array = (np.ascontiguousarray(v, dtype=np.uint8) for v in (states, mask, rule))
    pointers = [cuda.alloc(arr.nbytes) for arr in (state, mask_array, rule_array)]
    output = cuda.alloc(state.nbytes)
    count = cuda.alloc(ctypes.sizeof(ctypes.c_uint32))
    for pointer, arr in zip(pointers, (state, mask_array, rule_array)):
        cuda.upload(pointer, arr)
    return pointers, output, count, state


def _poison_bool_outputs(cuda: Cuda, output, count, n: int) -> None:
    """Make stale/partially-written output fail before every candidate call."""
    import numpy as np

    cuda.upload(output, np.full(n, 0xFF, dtype=np.uint8))
    cuda.upload(count, np.asarray([0xFFFFFFFF], dtype=np.uint32))


def _poison_float_output(cuda: Cuda, output, elements: int) -> None:
    """NaN poison ensures an omitted energy write cannot inherit a prior result."""
    import numpy as np

    cuda.upload(output, np.full(elements, np.nan, dtype=np.float32))


def _run_bool(cuda: Cuda, function, case, references):
    states, mask, rule = references.boolean_inputs(case)
    pointers, output, count, state = _new_bool_buffers(cuda, states, mask, rule)
    n, steps = int(case["parameters"]["n"]), int(case["parameters"]["steps"])
    _poison_bool_outputs(cuda, output, count, n)
    cuda.synchronize_device()
    _call_checked(function, [*pointers, n, steps, output, count, cuda.stream], "bool-transition")
    cuda.synchronize_device()
    actual = cuda.download(output, (n,), "uint8")
    actual_count = int(cuda.download(count, (1,), "uint32")[0])
    expected = references.boolean_epoch(states, mask, rule, steps)
    expected_count = sum(value == 3 for value in expected)
    return bool((actual == expected).all() and actual_count == expected_count)


def _run_energy(cuda: Cuda, function, case, references, *, weight_seed=None, keep_buffers=False):
    import numpy as np

    x_batches, weights = references.energy_inputs(case, weight_seed=weight_seed)
    x = _float32(x_batches)
    w = _float32(weights)
    params = case["parameters"]
    b, k, m, uses = (int(params[key]) for key in ("b", "k", "m", "uses"))
    x_device, w_device = cuda.alloc(x.nbytes), cuda.alloc(w.nbytes)
    out = cuda.alloc(uses * b * ctypes.sizeof(ctypes.c_float))
    cuda.upload(x_device, x)
    cuda.upload(w_device, w)
    _poison_float_output(cuda, out, uses * b)
    cuda.synchronize_device()
    _call_checked(function, [x_device, w_device, b, k, m, uses, out, cuda.stream, cuda.blas], "observable-energy")
    cuda.synchronize_device()
    actual = cuda.download(out, (uses * b,), "float32")
    expected = _energy_reference_numpy(x, w)
    passed = _check_float(actual, expected, 2e-4, 5e-5)
    if keep_buffers:
        return passed, (x_device, w_device, out, x, w)
    return passed


def _run_energy_updated(cuda: Cuda, function, case, references, original_seed: int, updated_seed: int) -> bool:
    """Call once, replace W on the same pointers, then call again in-process."""
    import numpy as np

    x_batches, original_weights = references.energy_inputs(case, weight_seed=original_seed)
    _x_again, updated_weights = references.energy_inputs(case, weight_seed=updated_seed)
    x, original, updated = _float32(x_batches), _float32(original_weights), _float32(updated_weights)
    p = case["parameters"]
    b, k, m, uses = (int(p[key]) for key in ("b", "k", "m", "uses"))
    x_device, w_device = cuda.alloc(x.nbytes), cuda.alloc(original.nbytes)
    output = cuda.alloc(uses * b * ctypes.sizeof(ctypes.c_float))
    cuda.upload(x_device, x)
    cuda.upload(w_device, original)
    args = [x_device, w_device, b, k, m, uses, output, cuda.stream, cuda.blas]
    _poison_float_output(cuda, output, uses * b)
    cuda.synchronize_device()
    _call_checked(function, args, "observable-energy initial-W validation")
    cuda.synchronize_device()
    first = cuda.download(output, (uses * b,), "float32")
    first_expected = _energy_reference_numpy(x, original)
    first_ok = _check_float(first, first_expected, 2e-4, 5e-5)
    # Reuse this process, function pointer, X allocation, W allocation and
    # output allocation. The changed seed is independent and may not be ignored.
    cuda.upload(w_device, updated)
    _poison_float_output(cuda, output, uses * b)
    cuda.synchronize_device()
    _call_checked(function, args, "observable-energy updated-W validation")
    cuda.synchronize_device()
    second = cuda.download(output, (uses * b,), "float32")
    second_expected = _energy_reference_numpy(x, updated)
    second_ok = _check_float(second, second_expected, 2e-4, 5e-5)
    distinguishable = not np.array_equal(first_expected, second_expected)
    return bool(first_ok and second_ok and distinguishable)


def _energy_guard_checks(cuda: Cuda, function, references) -> bool:
    """Run private validation-only all-zero, cancelling, and small-scale rows."""
    import numpy as np

    cases = [(np.asarray(x, dtype=np.float32), np.asarray(w, dtype=np.float32))
             for x, w in references.energy_guard_inputs()]
    for x, weights in cases:
        x_device, w_device = cuda.alloc(x.nbytes), cuda.alloc(weights.nbytes)
        output = cuda.alloc(ctypes.sizeof(ctypes.c_float))
        cuda.upload(x_device, x)
        cuda.upload(w_device, weights)
        _poison_float_output(cuda, output, 1)
        cuda.synchronize_device()
        _call_checked(function, [x_device, w_device, 1, 4, 3, 1, output, cuda.stream, cuda.blas], "observable-energy guard")
        cuda.synchronize_device()
        actual = cuda.download(output, (1,), "float32")
        expected = _energy_reference_numpy(x, weights)
        if not _check_float(actual, expected, 2e-4, 5e-5):
            return False
    return True


def _run_gemm(cuda: Cuda, function, case, references, *, warmup: int = 0, repetitions: int = 1):
    import numpy as np

    a_values, b_values, c_values = references.gemm_inputs(case)
    p = case["parameters"]
    m, n, k = (int(p[key]) for key in ("m", "n", "k"))
    alpha, beta = float(p["alpha"]), float(p["beta"])
    a, b, initial_c = (_float32(v) for v in (np.asarray(a_values).reshape(m, k),
                                              np.asarray(b_values).reshape(k, n),
                                              np.asarray(c_values).reshape(m, n)))
    a_device, b_device = cuda.alloc(a.nbytes), cuda.alloc(b.nbytes)
    c_device = cuda.alloc(initial_c.nbytes)
    cuda.upload(a_device, a)
    cuda.upload(b_device, b)
    reference = _gemm_reference_numpy(a, b, initial_c, alpha, beta)
    args = [a_device, b_device, c_device, m, n, k, alpha, beta, cuda.stream, cuda.blas]

    def invoke(*, timed: bool) -> float | None:
        # Restore the input C outside every measured interval, so beta has the
        # same semantics in warmup, correctness, and all repetitions.
        cuda.upload(c_device, initial_c)
        cuda.synchronize_device()
        start = time.perf_counter_ns() if timed else 0
        _call_checked(function, args, "dense-gemm")
        cuda.synchronize_device()
        elapsed = (time.perf_counter_ns() - start) / 1000.0 if timed else None
        actual = cuda.download(c_device, (m, n), "float32")
        if not _check_float(actual, reference, 2e-5, 5e-5):
            raise RuntimeError("dense candidate output changed or failed the reference during repeated calls")
        return elapsed

    for _ in range(warmup):
        invoke(timed=False)
    samples = [invoke(timed=True) for _ in range(repetitions)]
    return True, samples


def _validate(request: dict[str, Any], family: str, args) -> dict[str, Any]:
    import numpy as np

    refs = _references(args.references)
    library = _load_candidate(request)
    function = _load_family_api(library, family)
    rows = []
    failed: list[str] = []
    holdouts = _read(args.holdouts)
    with Cuda(args.cuda_lib_dir, args.cublas_lib_dir) as cuda:
        for case in request["cases"]:
            try:
                if family == "bool-transition":
                    passed = _run_bool(cuda, function, case, refs)
                elif family == "observable-energy":
                    passed = _run_energy(cuda, function, case, refs)
                else:
                    passed, _ = _run_gemm(cuda, function, case, refs)
            except Exception as exc:
                passed = False
                failed.append(f"public {case['id']}: {type(exc).__name__}: {exc}")
            rows.append({"case_id": case["id"], "workload_sha256": case["workload_sha256"],
                         "status": "pass" if passed else "fail"})
            if not passed and not any(item.startswith(f"public {case['id']}:") for item in failed):
                failed.append(f"public {case['id']}: numerical or semantic mismatch")

        private_rows = holdouts[family.replace("-", "_")]
        try:
            if family == "bool-transition":
                for case in private_rows:
                    if not _run_bool(cuda, function, case, refs):
                        failed.append(f"private {case['id']}: numerical or semantic mismatch")
            elif family == "observable-energy":
                for case in private_rows:
                    if "updated_w_seed" in case["input"]:
                        if not _run_energy_updated(cuda, function, case, refs,
                                                   int(case["input"]["w_seed"]),
                                                   int(case["input"]["updated_w_seed"])):
                            failed.append(f"private {case['id']}: updated-W call failed or produced stale output")
                    elif not _run_energy(cuda, function, case, refs):
                        failed.append(f"private {case['id']}: numerical mismatch")
                if not _energy_guard_checks(cuda, function, refs):
                    failed.append("private cancellation/all-zero/small-scale energy guards failed")
            else:
                for case in private_rows:
                    passed, _ = _run_gemm(cuda, function, case, refs)
                    if not passed:
                        failed.append(f"private {case['id']}: numerical mismatch")
        except Exception as exc:
            failed.append(f"private validation: {type(exc).__name__}: {exc}")
    return {
        "schema_version": 1,
        "request_id": request["request_id"],
        "status": "ok" if not failed else "error",
        "cases": rows,
        "private_checks": {"status": "pass" if not failed else "fail", "failures": failed},
        "reference_backend": {"numpy": np.__version__, "dtype": "float64 over represented float32 inputs"},
    }


def _benchmark(request: dict[str, Any], family: str, args) -> dict[str, Any]:
    refs = _references(args.references)
    library = _load_candidate(request)
    function = _load_family_api(library, family)
    case = request["case"]
    timing = request["timing"]
    warmup, repetitions = int(timing["warmup"]), int(timing["repetitions"])
    with Cuda(args.cuda_lib_dir, args.cublas_lib_dir) as cuda:
        if family == "dense-gemm":
            passed, samples = _run_gemm(cuda, function, case, refs, warmup=warmup, repetitions=repetitions)
            if not passed:
                raise RuntimeError("benchmark candidate failed the repeated dense result check")
        else:
            if family == "bool-transition":
                states, mask, rule = refs.boolean_inputs(case)
                pointers, output, count, _state = _new_bool_buffers(cuda, states, mask, rule)
                p = case["parameters"]
                expected = refs.boolean_epoch(states, mask, rule, int(p["steps"]))
                expected_count = sum(value == 3 for value in expected)
                invoke = lambda: _call_checked(function, [*pointers, int(p["n"]), int(p["steps"]),
                                                          output, count, cuda.stream], family)
            else:
                x_batches, weights = refs.energy_inputs(case)
                x, w = _float32(x_batches), _float32(weights)
                p = case["parameters"]
                b, k, m, uses = (int(p[key]) for key in ("b", "k", "m", "uses"))
                x_device, w_device = cuda.alloc(x.nbytes), cuda.alloc(w.nbytes)
                output = cuda.alloc(uses * b * ctypes.sizeof(ctypes.c_float))
                cuda.upload(x_device, x)
                cuda.upload(w_device, w)
                expected = _energy_reference_numpy(x, w)
                invoke = lambda: _call_checked(function, [x_device, w_device, b, k, m, uses,
                                                          output, cuda.stream, cuda.blas], family)
            for _ in range(warmup):
                if family == "bool-transition":
                    _poison_bool_outputs(cuda, output, count, int(p["n"]))
                else:
                    _poison_float_output(cuda, output, uses * b)
                cuda.synchronize_device()
                invoke()
                cuda.synchronize_device()
                if family == "bool-transition":
                    actual = cuda.download(output, (int(p["n"]),), "uint8")
                    actual_count = int(cuda.download(count, (1,), "uint32")[0])
                    valid = bool((actual == expected).all() and actual_count == expected_count)
                else:
                    actual = cuda.download(output, (uses * b,), "float32")
                    valid = _check_float(actual, expected, 2e-4, 5e-5)
                if not valid:
                    raise RuntimeError("candidate failed correctness during benchmark warmup")
            samples = []
            for _ in range(repetitions):
                if family == "bool-transition":
                    _poison_bool_outputs(cuda, output, count, int(p["n"]))
                else:
                    _poison_float_output(cuda, output, uses * b)
                cuda.synchronize_device()
                start = time.perf_counter_ns()
                invoke()
                cuda.synchronize_device()
                samples.append((time.perf_counter_ns() - start) / 1000.0)
                if family == "bool-transition":
                    actual = cuda.download(output, (int(p["n"]),), "uint8")
                    actual_count = int(cuda.download(count, (1,), "uint32")[0])
                    valid = bool((actual == expected).all() and actual_count == expected_count)
                else:
                    actual = cuda.download(output, (uses * b,), "float32")
                    valid = _check_float(actual, expected, 2e-4, 5e-5)
                if not valid:
                    raise RuntimeError("candidate failed correctness during repeated benchmark calls")
    return {
        "schema_version": 1,
        "request_id": request["request_id"],
        "status": "ok",
        "case_id": case["id"],
        "workload_sha256": case["workload_sha256"],
        "timing_scope": timing["scope"],
        "metric": timing["metric"],
        "unit": timing["unit"],
        "warmup": warmup,
        "repetitions": repetitions,
        "samples": samples,
    }


def _build(request: dict[str, Any], family: str, args) -> dict[str, Any]:
    source_dir = Path(request["candidate"]["source_dir"]).resolve(strict=True)
    source = source_dir / "kernel.cu"
    header = source_dir / "candidate_api.h"
    if not source.is_file() or not header.is_file():
        raise FileNotFoundError("candidate snapshot must contain top-level kernel.cu and candidate_api.h")
    build_dir = Path(request["build"]["directory"]).resolve(strict=True)
    artifact = build_dir / "candidate.so"
    target = request["target"].get("compiler_target", request["target"]["architecture"])
    command = [args.nvcc, "-std=c++17", "-O3", f"-arch={target}", "--shared", "-Xcompiler=-fPIC",
               "-I", str(source_dir), "-o", str(artifact), str(source),
               "-Xlinker", "-rpath", "-Xlinker", args.cuda_lib_dir,
               "-Xlinker", "-rpath", "-Xlinker", args.cublas_lib_dir]
    if family in {"observable-energy", "dense-gemm"}:
        command.append("-lcublas")
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(f"nvcc exited {completed.returncode}: {completed.stderr[-8000:]}")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    return {"schema_version": 1, "request_id": request["request_id"], "status": "ok",
            "artifacts": [{"path": artifact.name, "sha256": digest}]}


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("probe", "build", "validate", "benchmark"))
    parser.add_argument("--family", choices=("bool-transition", "observable-energy", "dense-gemm"), required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--holdouts", required=True)
    parser.add_argument("--cuda-lib-dir", required=True)
    parser.add_argument("--cublas-lib-dir", required=True)
    parser.add_argument("--nvcc", required=True)
    parser.add_argument("request")
    parser.add_argument("result")
    return parser.parse_args()


def main() -> int:
    args = _arguments()
    request = _read(args.request)
    request_id = request.get("request_id", "missing-request-id")
    try:
        if args.operation == "probe":
            with Cuda(args.cuda_lib_dir, args.cublas_lib_dir) as cuda:
                result = {"schema_version": 1, "request_id": request_id, "status": "ok",
                          "environment": _gpu_environment(cuda, args.nvcc)}
        elif args.operation == "build":
            result = _build(request, args.family, args)
        elif args.operation == "validate":
            result = _validate(request, args.family, args)
        else:
            result = _benchmark(request, args.family, args)
    except Exception as exc:
        result = {"schema_version": 1, "request_id": request_id, "status": "error",
                  "error": f"{type(exc).__name__}: {exc}", "traceback": traceback.format_exc(limit=5)}
    _write(args.result, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
