"""Independent CPU input generation and correctness references for KB-04.

This module is evaluator material. It is not part of the installed skill or
the candidate-visible bundle.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from typing import Any

_MASK64 = (1 << 64) - 1
_GOLDEN = 0x9E3779B97F4A7C15


def splitmix64(value: int) -> int:
    """Return one stable SplitMix64 output, independent of Python hash state."""
    z = (value + _GOLDEN) & _MASK64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & _MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & _MASK64
    return (z ^ (z >> 31)) & _MASK64


def represented_f32(seed: int, index: int, lane: int = 0) -> float:
    """Generate an exactly represented FP32 dyadic value in [-0.5, 0.5]."""
    raw = splitmix64((seed + index * _GOLDEN + lane * 0xD1B54A32D192ED03) & _MASK64)
    numerator = int(raw % 1025) - 512
    return numerator / 1024.0


def _de_bruijn_cycle(alphabet: int, order: int) -> list[int]:
    work = [0] * (alphabet * order)
    sequence: list[int] = []

    def visit(t: int, period: int) -> None:
        if t > order:
            if order % period == 0:
                sequence.extend(work[1:period + 1])
            return
        work[t] = work[t - period]
        visit(t + 1, period)
        for value in range(work[t - period] + 1, alphabet):
            work[t] = value
            visit(t + 1, t)

    visit(1, 1)
    return sequence


def boolean_inputs(case: dict[str, Any]) -> tuple[list[int], list[int], list[int]]:
    parameters = case["parameters"]
    input_spec = case["input"]
    n = int(parameters["n"])
    seed = int(input_spec.get("seed", 0))
    rule_seed = int(input_spec["rule_seed"])
    if input_spec.get("pattern") == "debruijn-pairs-mask-halves-v1":
        cycle = _de_bruijn_cycle(4, 2)
        if n != 2 * len(cycle):
            raise ValueError("the all-local-tuples pattern requires n=32")
        states = cycle + cycle
        mask = [0] * len(cycle) + [1] * len(cycle)
    else:
        states = [splitmix64(seed + i * _GOLDEN) & 3 for i in range(n)]
        mask = [splitmix64(seed ^ (i * 0xD1B54A32D192ED03)) & 1 for i in range(n)]
    rule = [splitmix64(rule_seed + i * _GOLDEN) & 3 for i in range(32)]
    rule[:4] = [0, 1, 2, 3]
    return states, mask, rule


def boolean_step(states: Sequence[int], mask: Sequence[int], rule: Sequence[int]) -> list[int]:
    if not states or len(states) != len(mask) or len(rule) != 32:
        raise ValueError("expected non-empty states/mask of equal length and a 32-entry rule")
    n = len(states)
    if any(value not in range(4) for value in states) or any(value not in (0, 1) for value in mask):
        raise ValueError("state values must be 0..3 and mask values must be 0..1")
    if any(value not in range(4) for value in rule):
        raise ValueError("rule outputs must be 0..3")
    old = list(states)
    return [rule[(old[i] * 4 + old[(i - 1) % n]) * 2 + mask[i]] for i in range(n)]


def boolean_epoch(states: Sequence[int], mask: Sequence[int], rule: Sequence[int], steps: int) -> list[int]:
    if steps < 0:
        raise ValueError("steps must be non-negative")
    current = list(states)
    for _ in range(steps):
        current = boolean_step(current, mask, rule)
    return current


def energy_inputs(case: dict[str, Any], *, weight_seed: int | None = None) -> tuple[list[list[list[float]]], list[list[float]]]:
    p = case["parameters"]
    spec = case["input"]
    batch = int(p["b"])
    k = int(p["k"])
    m = int(p["m"])
    uses = int(p["uses"])
    x_seed = int(spec["x_seed"])
    w_seed = int(spec["w_seed"] if weight_seed is None else weight_seed)
    x_values = [represented_f32(x_seed, i, lane=use + 1)
                for use in range(uses) for i in range(batch * k)]
    x_batches = []
    cursor = 0
    for _ in range(uses):
        rows = []
        for _ in range(batch):
            rows.append(x_values[cursor:cursor + k])
            cursor += k
        x_batches.append(rows)
    weights = [[represented_f32(w_seed, i * m + j, lane=11)
                for j in range(m)] for i in range(k)]
    return x_batches, weights


def energy_guard_inputs() -> list[tuple[list[list[list[float]]], list[list[float]]]]:
    """Validation-only represented inputs for zero, cancellation and scale guards."""
    scale = 2.0 ** -12
    return [
        ([[[0.0, 0.0, 0.0, 0.0]]], [[0.0, 0.0, 0.0] for _ in range(4)]),
        ([[[0.25, 0.25, 0.25, 0.25]]],
         [[0.25, 0.25, 0.25], [-0.25, 0.25, -0.25],
          [0.25, -0.25, -0.25], [-0.25, -0.25, 0.25]]),
        ([[[scale, scale, scale, scale]]],
         [[scale, 0.0, scale], [-scale, 0.0, scale],
          [scale, 0.0, scale], [-scale, 0.0, scale]]),
    ]


def observe_energy(x_batches: Sequence[Sequence[Sequence[float]]],
                   weights: Sequence[Sequence[float]]) -> list[list[float]]:
    if not x_batches or not weights or not weights[0]:
        raise ValueError("X and W must be non-empty")
    k = len(weights)
    m = len(weights[0])
    if any(len(row) != m for row in weights):
        raise ValueError("W must be rectangular")
    result: list[list[float]] = []
    for batch in x_batches:
        energies = []
        for row in batch:
            if len(row) != k:
                raise ValueError("each X row must match W's input dimension")
            response = [math.fsum(float(row[t]) * float(weights[t][j]) for t in range(k))
                        for j in range(m)]
            energies.append(math.fsum(value * value for value in response))
        result.append(energies)
    return result


def gemm_inputs(case: dict[str, Any]) -> tuple[list[float], list[float], list[float]]:
    p = case["parameters"]
    spec = case["input"]
    m, n, k = int(p["m"]), int(p["n"]), int(p["k"])
    a = [represented_f32(int(spec["a_seed"]), i, lane=21) for i in range(m * k)]
    b = [represented_f32(int(spec["b_seed"]), i, lane=22) for i in range(k * n)]
    c = [represented_f32(int(spec["c_seed"]), i, lane=23) for i in range(m * n)]
    return a, b, c


def gemm_reference(a: Sequence[float], b: Sequence[float], c: Sequence[float],
                   m: int, n: int, k: int, alpha: float, beta: float) -> list[float]:
    if min(m, n, k) <= 0 or len(a) != m * k or len(b) != k * n or len(c) != m * n:
        raise ValueError("matrix storage lengths do not match positive row-major dimensions")
    out = [0.0] * (m * n)
    for i in range(m):
        arow = a[i * k:(i + 1) * k]
        for j in range(n):
            dot = math.fsum(float(arow[t]) * float(b[t * n + j]) for t in range(k))
            index = i * n + j
            out[index] = float(alpha) * dot + float(beta) * float(c[index])
    return out


def within_tolerance(actual: Iterable[float], expected: Iterable[float],
                     *, absolute: float, relative: float) -> bool:
    actual_values = list(actual)
    expected_values = list(expected)
    if len(actual_values) != len(expected_values):
        return False
    return all(math.isfinite(float(a)) and math.isfinite(float(e)) and
               abs(float(a) - float(e)) <= absolute + relative * abs(float(e))
               for a, e in zip(actual_values, expected_values))
