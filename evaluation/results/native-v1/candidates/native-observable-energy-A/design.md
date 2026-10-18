# Native observable-energy candidate design

The required output for each flattened query row x is

    energy = sum_m (sum_k x[k] * W[k,m])^2.

All rows are required, W may change on every call, and the reference evaluates the represented FP32 inputs in binary64. The fixed acceptance tolerance is absolute 2e-4 plus relative 5e-5.

The implementation uses two exact algebraic routes under the same single-precision arithmetic contract. For short epochs it computes each response directly, accumulates its square, and writes one energy per row in a single fused kernel. This avoids response scratch and a second kernel launch. For epochs where the arithmetic model favors reuse and a cuBLAS handle is available, it forms G = W*W^T for this call, computes X*G for every flattened query row, and reduces x dot (x*G). The identity x*G*x^T = sum_m (x*W[:,m])^2 preserves the requested observable. G and projected rows live in one temporary allocation and are freed before return; no state survives a call.

The dispatch compares leading arithmetic counts. Direct work is proportional to R*K*M. The Gram route is proportional to K*K*M + R*K*K, where R is batch_rows*uses. It selects Gram only when M>K and R > (K*M)/(M-K), and otherwise uses direct work. This comparison ignores launch, allocation, cache, and library efficiency, so it is a plausible generic crossover model rather than a measured performance boundary. If no cuBLAS handle is supplied, the direct route supports the public API contract.

The cuBLAS calls run on the caller stream. Row-major W is passed as column-major W transpose, making A^T*A the K by K Gram matrix. Since G is symmetric, column-major G*X^T is stored as row-major X*G. The direct and projected routes write every flattened output row.

The source compiled for sm_70 with the supplied CPU-only build wrapper. No GPU execution, correctness comparison against the independent reference, runtime error test, or timing was available. The Gram route reassociates FP32 operations and both routes reduce in FP32, so acceptance under the fixed tolerance remains unverified. The operation-count crossover and performance benefit are hypotheses, not benchmark results.
