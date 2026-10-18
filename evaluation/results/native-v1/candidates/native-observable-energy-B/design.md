# Observable energy candidate design

The required output for one query row is

sum_m (sum_k x[k] * W[k,m])^2 = x * (W * W^T) * x^T.

The response matrix is not observable, and W is fixed only within this call. The candidate recomputes G = W * W^T on every eligible epoch; it keeps no state across calls. For short epochs, or when the optional cuBLAS handle is null, one CUDA CTA computes the response values and reduces their squares directly. When a handle exists and the simple multiply-add count favors preparation, cuBLAS forms G and one CTA per query row evaluates x * G * x^T. The transformed path allocates only the K-by-K Gram matrix and never writes the K-by-M response or an xG intermediate.

The dispatch compares direct work rows*K*M with transformed work K*M*K + rows*K*K. This is a shape-based arithmetic heuristic, not a measured crossover. Both routes use FP32 reassociation, which the contract allows only within its fixed binary64-reference tolerance. The cuBLAS path temporarily sets the supplied handle's stream and scalar pointer mode, then restores both. Allocation, Gram preparation, query evaluation, and free all occur inside the call's epoch cost.

The first rejection test is the evaluator's independent binary64 comparison on all three declared workloads, including a second call with changed W. It must establish the stated tolerance separately for the direct and Gram paths before timing can support an advantage claim. The only executed validation here was the permitted sm_70 NVCC shared-library build; no runtime correctness or performance result is available.
