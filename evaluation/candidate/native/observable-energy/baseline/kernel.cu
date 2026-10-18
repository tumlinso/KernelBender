#include "candidate_api.h"

#include <cuda_runtime.h>
#include <cublas_v2.h>

namespace {
__global__ void squared_row_sums(const float *responses, float *energies,
                                 int rows, int width) {
    const int row = blockIdx.x;
    if (row >= rows) return;
    __shared__ float partial[256];
    const int tid = threadIdx.x;
    float sum = 0.0f;
    for (int j = tid; j < width; j += blockDim.x) {
        const float value = responses[static_cast<size_t>(row) * width + j];
        sum = fmaf(value, value, sum);
    }
    partial[tid] = sum;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (tid < stride) partial[tid] += partial[tid + stride];
        __syncthreads();
    }
    if (tid == 0) energies[row] = partial[0];
}
}  // namespace

extern "C" int kb_run(const float *x_batches, const float *weights,
                      int batch_rows, int input_width, int output_width,
                      int uses, float *energies, void *raw_stream,
                      void *raw_blas_handle) {
    if (!x_batches || !weights || !energies || batch_rows <= 0 || input_width <= 0 ||
        output_width <= 0 || uses <= 0 || !raw_blas_handle)
        return static_cast<int>(cudaErrorInvalidValue);
    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);
    const cublasHandle_t handle = static_cast<cublasHandle_t>(raw_blas_handle);
    const int total_rows = batch_rows * uses;
    cublasStatus_t status = cublasSetStream(handle, stream);
    if (status != CUBLAS_STATUS_SUCCESS) return 1000 + static_cast<int>(status);
    float *responses = nullptr;
    // All U batches are flattened into one GEMM, so scratch must cover every
    // row in the epoch, not just one batch.
    cudaError_t error = cudaMalloc(&responses, static_cast<size_t>(total_rows) * output_width * sizeof(float));
    if (error != cudaSuccess) return static_cast<int>(error);

    const float alpha = 1.0f;
    const float beta = 0.0f;
    // Flatten contiguous X[U,B,K] and perform one direct GEMM for the epoch.
    // Row-major X*W is column-major W^T*X^T in the same storage.
    status = cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                         output_width, total_rows, input_width,
                         &alpha, weights, output_width,
                         x_batches, input_width, &beta, responses, output_width);
    if (status != CUBLAS_STATUS_SUCCESS) {
        cudaFree(responses);
        return 1000 + static_cast<int>(status);
    }
    squared_row_sums<<<total_rows, 256, 0, stream>>>(responses, energies,
                                                     total_rows, output_width);
    error = cudaPeekAtLastError();
    cudaError_t free_error = cudaFree(responses);
    if (error != cudaSuccess) return static_cast<int>(error);
    return static_cast<int>(free_error);
}
