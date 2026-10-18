# Boolean transition candidate design

The operation is the periodic synchronous transition

`next[i] = rule[(state[i] * 4 + state[(i - 1) mod N]) * 2 + mask[i]]`,

repeated for `steps` transitions, followed by exact output bytes and a count of
final values equal to 3. The rule and mask are read from the caller on every
invocation; no state persists between calls.

For `steps == 1`, one direct kernel computes every output and its local count.
For up to 128 steps, a fused tiled kernel assigns each CTA up to 1024 consecutive
outputs. It stages a left halo of `steps` bytes plus the output tile and mask in
shared memory. At transition `s`, it updates local positions `j >= s`; therefore
the `steps`-deep halo supplies the full causal cone for the tile. The final tile
is stored from local positions `[steps, steps + output_count)`. The initial
loads wrap with positive modulo, including for a tile whose halo crosses the
periodic boundary.

Each CTA reduces its final count. A single-CTA call writes the count directly;
multiple CTAs first zero the count on the caller stream, then add one partial per
CTA. Tails use the actual output count, so they neither read nor write beyond
`N`. For more than 128 steps, a scalar ping-pong fallback preserves the full
epoch semantics and fuses the count into its last transition. It allocates two
per-call scratch buffers and keeps all launches on the caller stream.

The CUDA skill's machine-aligned design guide points to bit-sliced state for
finite categorical transitions. M06 and C02 explain the potential persistent
Boolean representation and its transpose costs. This candidate instead keeps
byte state in shared memory across the epoch: the rule is an arbitrary runtime
lookup, and no device measurements were available to establish that packing and
unpacking bitplanes would repay their conversion cost here. This is a design
choice, not a measured comparison.

Compilation succeeded once for `sm_70`. The isolated environment exposes no GPU
runtime, so output correctness, launch behavior, timing, and memory use were not
executed or measured. Correctness claims above follow from the transition
window and indexing argument only.
