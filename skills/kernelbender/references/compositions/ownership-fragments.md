# Composition: carry producer ownership into the consumer

**Use when:** a kernel writes or converts a complete intermediate representation chiefly so the next stage can read it in a canonical layout. Compose ownership maps of adjacent stages and keep the representation that makes the full pipeline easiest to execute.

## Write the map

For each semantic value with coordinate `x`, record its producer owner `P(x)=(lane,register_slot)` or a larger tuple that includes warp, shared bank and fragment coordinate. Record the consumer's desired owner `Q(x)`. For values with one producer, the required communication is the map `Q ∘ P⁻¹`. If the consumer's retile is the inverse of a preceding canonicalization, those two maps cancel. If only a subset is used, move just that subset. If a value is replicated, record all owners and the later selection or reduction.

For a middle operation `f`, a common permutation can pass through when `f(p(x))=p(f(x))` and all coefficients, masks and indices follow the same map. This is often true for elementwise operations. It can fail for reductions, index-sensitive nonlinearities, boundary rules or collectives that expect another participant group. Validate the equation and the map independently. (Atlas M04, M18, M25; C16, C36.)

## Keep a useful distributed result

An explicit PTX tensor form may produce a result whose ownership is directly useful to a second stage, mask or output projection. Preserving it can remove a canonical store, reload and transpose. The exact form's coordinate map comes from `hw-volta-mma`; raw WMMA fragment slots remain opaque. Atlas E09 validated coordinates of its explicit form while it did not establish general WMMA raw ownership. A non-tensor example is a warp lane that owns a stable local vertex and uses a mask or shuffle to route the next state. A shared-memory swizzle can also feed its consumer directly if both stages agree on that bank map.

This is not a general register-file exchange. The receiving lane must be a defined participant, source values must exist, and wider values need more moves. Matching matrix dimensions do not guarantee accumulator/operand ownership compatibility. Use `hw-volta-participation` and `hw-volta-mma` for the exact Volta forms, then retrieve corresponding target pages elsewhere.

## Compare the full producer-to-consumer path

Keep the canonical/materialized route as a strong control. Count writes, reads, intermediate allocation, shuffles, shared exchanges, barriers, padding, conversion, address calculations, live registers and spills. A deleted memory pass can be replaced by a longer dependency chain or lower useful residency. Compare the same arithmetic and output semantics, and include final materialization where the caller observes it.

The first experiment assigns unique labels or one-hot values to coordinates so every source and destination is visible. Then test the actual operator/numerical contract with arithmetic fixed. Compare complete producer-to-consumer execution and inspect generated ownership only for a concrete mapping uncertainty. Fewer conversion calls in source are not a performance result.

## Restore a boundary if it is useful

Reject the composition when it assumes an inverse map that is not defined, or when intended fanout, gather, replication or reduction lacks an explicit routing and combination contract. Collective participants also need defined operands, reduction axes must remain correct, and retained state must stay within a practical resource budget. Keep the materialized boundary when it shortens live ranges or enables a much better library path. Exact output type and rounding can alter the consumer map. The relevant KernelWiki routes are `hw-volta-mma`, `hw-volta-participation`, `hw-volta-resources`, `hw-volta-numerics` and `hw-volta-operand-delivery`.

Atlas IDs: M04, M12–M13, M18–M19, M24–M25; C10, C16–C17, C36; E04, E06, E09. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
