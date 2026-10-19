# Composition: screen a decision, then refine only ambiguity

**Use when:** the caller needs an exact predicate, ranked shortlist or selected subset, while many inputs are expected to lie far from a decision boundary and a cheaper estimate can be rigorously bounded. This composes a fast approximate stage with exact work without changing the final answer.

## Construction

For a score `s` and threshold `τ`, assume a candidate fast path computes `ŝ` and a valid bound holds for every allowed input:

```text
|s - ŝ| <= ε
accept  if ŝ - ε >= τ
reject  if ŝ + ε <  τ
refine  otherwise
```

The accept/reject decisions are exact for the defined predicate. Store ambiguous positions in a mask, compact them if needed, and evaluate the reference computation only there. The proof for `ε` must include input quantization, approximating function, instruction accumulation, table/filter rounding and output extraction. If a proof is unavailable, describe the method as an approximate algorithm only if the caller has permitted that change.

This can compose with a tensor/block score, table interpolation, bitset prefilter or low-precision dot. The ambiguity mask can use the positional-routing construction; the exact fallback may use higher precision, integer arithmetic or the established library. Keep the original exact path for all ambiguous elements. (Atlas M02, M10, M23, M28; C14, C31.)

## Economic test

Let `p` be the ambiguous fraction, `F` the cheap filter cost, `R` the refinement cost for an ambiguous element, and `Q` the queue/compaction cost. The average cost is approximately `F + Q + p*R`, plus any amortized setup and final ordering cost. Direct exact cost `D` is the control. The screen has a possible cost advantage only when `F+Q+pR < D` at the caller's actual shape and input distribution. Use the same observable output and include selected-item materialization. If most cases refine, the filter can add overhead while preserving all original work.

The exact consumer matters. If it needs every score, screening has less room to avoid work; if it needs only membership, omitting full scores can also remove an intermediate. If it needs a stable sorted top-k, include ordering/selection costs and tie semantics. The estimate must not silently loosen the decision contract.

## Baselines, tests and falsifiers

Keep direct exact evaluation and a simpler conservative integer/bitset filter as controls. First test adversarial values at `τ`, at `τ±ε`, on approximation domain endpoints, and at every exceptional input. Independently validate the bound over its formal domain; finite sampling can find bugs but does not prove a bound. Measure ambiguity rate and full fast+refine latency across distributions both far from and concentrated near the boundary. Reject the speed hypothesis if exact work is not avoided enough to repay the filter, queue and dispatch. Reject exactness claims if any source of error is missing from `ε`.

For a table or texture-derived estimate, also test coordinate representation, interpolation and table conversion. For tensor scores, retrieve the precise target's numerical page and retain its tested scope. For a screen based on a statistical margin, the result is not certified unless the margin is a proven bound for the task's input domain.

**Evidence boundary:** Atlas E26 measured finite sampled function errors but established no global bound and did not implement a screen/refine path. E11's bounded dense intersection result is not evidence that a numeric screen pays off. E39's uncertain bitplane addition result is another operator and does not establish a screening crossover. The composition itself remains unmeasured. Use `hw-volta-numerics` as an exact architecture route, not a source of an error certificate for your new function.

Atlas IDs: M02, M10, M23, M28; C14, C31; E10, E11, E26, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
