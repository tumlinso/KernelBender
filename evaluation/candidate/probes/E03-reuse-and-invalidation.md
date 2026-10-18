# E03 — Reuse a packed parameter without assuming it is immutable forever

The caller stores signed four-bit weights `q` in `[-8,7]` for a logical
row-major matrix `W[K,M]`, with one positive FP32 scale per consecutive
32-element block along `M`. The represented weight is the FP32 product
`float(q) * scale`; no extra rounding is permitted during decoding. Two
consumers use the same weights during an epoch:

1. `Y = X*W`, where `X` is `[8,K]` and the full `[8,M]` FP32 output is
   required.
2. `Z = V*W^T`, where `V` is `[8,M]` and the full `[8,K]` FP32 output is
   required.

Use `K=64`, `M=128`. An epoch contains either 1 or 64 pairs of query batches.
The packed weights and scales change between epochs, remain unchanged within
one epoch, and may be read concurrently by both consumers. Inputs are finite
FP32 values in `[-0.5,0.5]`; both outputs must match direct FP32 accumulation
of the represented weights within `atol=2e-4, rtol=2e-4`.

Compare direct decoding with shared preparation or another concrete layout.
State who owns prepared data, how both consumers use it, and when an update
invalidates it. Include preparation, storage, both consumers, and update cost
for the full epoch. Do not infer a long reuse lifetime from the maximum-use
case alone.
