# E01 — Compute only what the consumer observes

You receive a row-major FP32 matrix `X` with shape `[B,K]` and two row-major
FP32 parameter matrices `A[K,M]` and `B[M,P]`. The caller needs only
`energy[b] = sum_p (sum_m (sum_k X[b,k] * A[k,m]) * B[m,p])^2` for every row
`b`; neither intermediate is observable. `A` and `B` remain fixed for an
epoch containing either 1 or 32 query batches. They are replaced before the
next epoch. Inputs are arbitrary finite values in `[-0.5,0.5]`; FP32 output
must match the direct FP32 operator within `atol=2e-4, rtol=2e-4`. Reordering
is allowed within that bound.

Return a concise design brief with the strongest conventional route, one
materially different feasible construction if justified, the complete epoch
cost including preparation and updates, and a test that could reject the
recommendation. Then explain how the decision changes if the caller requires
the intermediate `X*A` rounded to FP32 before applying `B`, or if parameters
change after every batch. Do not assume a faster design must exist.
