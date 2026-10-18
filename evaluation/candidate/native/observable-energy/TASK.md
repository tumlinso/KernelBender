# Native task: squared response energy

## Operation

For one update epoch, `W` is a row-major FP32 matrix `[K,M]`. The caller
provides `U` query batches, each a row-major FP32 matrix `[B,K]`. For every
use `u` and row `b`, return
`energy[u,b] = sum_m (sum_k X[u,b,k] * W[k,m])^2`. Only the energy is
observable; the intermediate response is not. All `U*B` outputs are required.
`W` is unchanged during one call and may be replaced before the next call.
The full call covers one update epoch, including every preparation and all
`U` query uses.

The public API is `kb_run` in `candidate_api.h`. Its X, W, and output pointers
are device addresses; `stream` is caller-owned and `blas_handle` is a
caller-created cuBLAS handle or null. The function must write every output
and may not reuse hidden state across calls. The evaluator calls it again with
changed W values to check update handling.

The public inputs are finite FP32 values generated from the declared seeds in
`cases.json`; the common range is `[-0.5,0.5]`. The trusted CPU reference
computes each response and energy in binary64 over the represented FP32
inputs. Acceptance is `abs(actual-reference) <= 2e-4 + 5e-5*abs(reference)`.
This tolerance is fixed before tuning. Reassociation is allowed within it.

## Workloads and objective

Three cases compare a short epoch with one low-work use, one large use, and a
long-reuse epoch at the large shape. `B` is query rows per use, `K` the input
width, `M` the response width, and `U` uses per unchanged W. The exact values
are in `cases.json`. The primary objective is full update-epoch latency per
call, including temporary allocation, preparation, conversion, all query
uses, and output generation. Inputs and output buffers are resident on the
GPU before the call. Report device memory separately.

The corrected baseline flattens the contiguous `U*B` rows into one direct FP32
cuBLAS SGEMM, followed by a reduction of the squared responses. Any
reformulation is permitted when it meets the same fixed tolerance and keeps
its preparation and update costs inside the measured epoch.
