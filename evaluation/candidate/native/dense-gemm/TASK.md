# Native control: regular dense GEMM

Compute row-major FP32 `C = alpha*A*B + beta*C` for arbitrary represented
inputs and return the full output matrix. The first case is square and the
second rectangular; exact dimensions, seeds, and coefficients are in
`cases.json`. Inputs are finite FP32 values in `[-0.5,0.5]`. The CPU oracle
evaluates each dot product and the alpha/beta combination in binary64 over
those represented values. Acceptance is
`abs(actual-reference) <= 2e-5 + 5e-5*abs(reference)`.

The `kb_run` API in `candidate_api.h` receives device pointers, a caller-owned
CUDA stream, and a caller-created cuBLAS handle (or null for a custom route).
All C outputs must be written. Input/output matrix C is initialized for each
call. The API call's complete latency is the metric; scratch allocation and
all work performed by the candidate are included. Host input setup and copies
to device are excluded.

There is no hidden sparsity, fixed value pattern, reduced output, or permission
to change arithmetic semantics. A correct recommendation to retain the
cuBLAS SGEMM baseline is a successful control outcome. Unnecessary design and
implementation cost is recorded separately from timing.
