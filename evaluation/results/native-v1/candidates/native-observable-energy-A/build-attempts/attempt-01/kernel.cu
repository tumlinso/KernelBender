#include "candidate_api.h"

#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <stddef.h>
#include <stdint.h>

namespace {
constexpr int kBlockThreads = 256;

__device__ __forceinline__ float block_sum(float value) {
    __shared__ float partial[kBlockThreads];
    const int tid = threadIdx.x;
    partial[tid] = value;
    __syncthreads();
    for (int stride = kBlockThreads / 2; stride > 0; stride >>= 1) {
        if (tid < stride) partial[tid] += partial[tid + stride];
        __syncthreads();
    }
    return partial[0];
}

// Direct path: compute each response and immediately fold its square into
// the row result, avoiding a full response matrix and a second launch.
__global__ void direct_energy(const float *x, const float *weights,
                             float *energies, int rows, int k, int m) {
    const int row = blockIdx.x;
    if (row >= rows) return;
    const float *xrow = x + static_cast<size_t>(row) * k;
    float local = 0.0f;
    for (int col = threadIdx.x; col < m; col += blockDim.x) {
        float response = 0.0f;
        for (int q = 0; q < k; ++q) {
            response = fmaf(xrow[q],
                            weights[static_cast<size_t>(q) * m + col],
                            response);
        }
        local = fmaf(response, response, local);
    }
    const float total = block_sum(local);
    if (threadIdx.x == 0) energies[row] = total;
}

__global__ void projected_energy(const float *x, const float *projected,
                                 float *energies, int rows, int k) {
    const int row = blockIdx.x;
    if (row >= rows) return;
    const size_t offset = static_cast<size_t>(row) * k;
    float local = 0.0f;
    for (int col = threadIdx.x; col < k; col += blockDim.x) {
        local = fmaf(x[offset + col], projected[offset + col], local);
    }
    const float total = block_sum(local);
    if (threadIdx.x == 0) energies[row] = total;
}
}  // namespace

extern "C" int kb_run(const float *x_batches, const float *weights,
                      int batch_rows, int input_width, int output_width,
                      int uses, float *energies, void *raw_stream,
                      void *raw_blas_handle) {
    if (!x_batches || !weights || !energies || batch_rows <= 0 ||
        input_width <= 0 || output_width <= 0 || uses <= 0 ||
        uses > INT32_MAX / batch_rows) {
        return static_cast<int>(cudaErrorInvalidValue);
    }

    const int rows = batch_rows * uses;
    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);

    // The Gram reformulation is worthwhile only when its extra preparation
    // work is amortized across enough rows. This compares operation counts:
    // direct is R*K*M; Gram plus queries is K*K*M + R*K*K.
    const int64_t k = input_width;
    const int64_t m = output_width;
    const int64_t r = rows;
    const bool gram_is_cheaper =
        m > k && r > (k * m) / (m - k);

    if (!gram_is_cheaper || !raw_blas_handle) {
        direct_energy<<<rows, kBlockThreads, 0, stream>>>(
            x_batches, weights, energies, rows, input_width, output_width);
        return static_cast<int>(cudaPeekAtLastError());
    }

    const cublasHandle_t handle =
        static_cast<cublasHandle_t>(raw_blas_handle);
    cublasStatus_t status = cublasSetStream(handle, stream);
    if (status != CUBLAS_STATUS_SUCCESS) {
        return 1000 + static_cast<int>(status);
    }

    const size_t max_size = ~static_cast<size_t>(0);
    const size_t k_size = static_cast<size_t>(input_width);
    const size_t row_size = static_cast<size_t>(rows);
    if (k_size > max_size / k_size || row_size > max_size / k_size) {
        return static_cast<int>(cudaErrorInvalidValue);
    }
    const size_t gram_count = k_size * k_size;
    const size_t projected_count = row_size * k_size;
    if (gram_count > max_size - projected_count ||
        gram_count + projected_count > max_size / sizeof(float)) {
        return static_cast<int>(cudaErrorInvalidValue);
    }

    float *scratch = nullptr;
    cudaError_t error =
        cudaMalloc(&scratch, (gram_count + projected_count) * sizeof(float));
    if (error != cudaSuccess) return static_cast<int>(error);
    float *gram = scratch;
    float *projected = scratch + gram_count;

    const float alpha = 1.0f;
    const float beta = 0.0f;

    // weights are row-major [K,M], hence column-major [M,K]. A^T*A
    // produces the symmetric K-by-K matrix W*W^T.
    status = cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_N,
                         input_width, input_width, output_width,
                         &alpha, weights, output_width,
                         weights, output_width, &beta, gram, input_width);
    if (status != CUBLAS_STATUS_SUCCESS) {
        cudaFree(scratch);
        return 1000 + static_cast<int>(status);
    }

    // Column-major G*X^T is stored as row-major (X*G) in the same buffer.
    status = cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N,
                         input_width, rows, input_width,
                         &alpha, gram, input_width,
                         x_batches, input_width, &beta,
                         projected, input_width);
    if (status != CUBLAS_STATUS_SUCCESS) {
        cudaFree(scratch);
        return 1000 + static_cast<int>(status);
    }

    projected_energy<<<rows, kBlockThreads, 0, stream>>>(
        x_batches, projected, energies, rows, input_width);
    error = cudaPeekAtLastError();
    const cudaError_t free_error = cudaFree(scratch);
    if (error != cudaSuccess) return static_cast<int>(error);
    return static_cast<int>(free_error);
}
