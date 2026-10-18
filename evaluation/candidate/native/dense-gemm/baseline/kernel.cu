#include "candidate_api.h"

#include <cuda_runtime.h>
#include <cublas_v2.h>

extern "C" int kb_run(const float *a, const float *b, float *c,
                      int m, int n, int k, float alpha, float beta,
                      void *raw_stream, void *raw_blas_handle) {
    if (!a || !b || !c || m <= 0 || n <= 0 || k <= 0 || !raw_blas_handle)
        return static_cast<int>(cudaErrorInvalidValue);
    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);
    const cublasHandle_t handle = static_cast<cublasHandle_t>(raw_blas_handle);
    cublasStatus_t status = cublasSetStream(handle, stream);
    if (status != CUBLAS_STATUS_SUCCESS) return 1000 + static_cast<int>(status);
    // Row-major C=A*B is column-major C^T=B^T*A^T in the same storage.
    status = cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                         n, m, k, &alpha, b, n, a, k, &beta, c, n);
    return status == CUBLAS_STATUS_SUCCESS ? 0 : 1000 + static_cast<int>(status);
}
