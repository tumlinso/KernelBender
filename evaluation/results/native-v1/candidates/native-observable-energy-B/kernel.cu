#include "candidate_api.h"

#include <cuda_runtime.h>
#include <cublas_v2.h>

#include <climits>
#include <cstddef>

namespace {

__global__ void direct_energy(const float *x, const float *weights,
                              float *energies, int rows, int k_width,
                              int m_width) {
    const int row = blockIdx.x;
    if (row >= rows) return;

    __shared__ float partial[256];
    const int tid = threadIdx.x;
    float sum = 0.0f;
    const size_t x_base = static_cast<size_t>(row) * k_width;
    for (int m = tid; m < m_width; m += blockDim.x) {
        float response = 0.0f;
        for (int k = 0; k < k_width; ++k) {
            response = fmaf(x[x_base + k],
                            weights[static_cast<size_t>(k) * m_width + m],
                            response);
        }
        sum = fmaf(response, response, sum);
    }
    partial[tid] = sum;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (tid < stride) partial[tid] += partial[tid + stride];
        __syncthreads();
    }
    if (tid == 0) energies[row] = partial[0];
}

// Compute x * (W W^T) * x^T without materializing either response or xG.
// Each CTA owns one output row; adjacent lanes read adjacent Gram columns.
__global__ void gram_energy(const float *x, const float *gram,
                            float *energies, int rows, int k_width) {
    const int row = blockIdx.x;
    if (row >= rows) return;

    __shared__ float partial[128];
    const int tid = threadIdx.x;
    const size_t x_base = static_cast<size_t>(row) * k_width;
    float sum = 0.0f;
    for (int col = tid; col < k_width; col += blockDim.x) {
        float projected = 0.0f;
        for (int k = 0; k < k_width; ++k) {
            projected = fmaf(x[x_base + k],
                              gram[static_cast<size_t>(k) * k_width + col],
                              projected);
        }
        sum = fmaf(x[x_base + col], projected, sum);
    }
    partial[tid] = sum;
    __syncthreads();
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (tid < stride) partial[tid] += partial[tid + stride];
        __syncthreads();
    }
    if (tid == 0) energies[row] = partial[0];
}

int cublas_error(cublasStatus_t status) {
    return 1000 + static_cast<int>(status);
}

}  // namespace

extern "C" int kb_run(const float *x_batches, const float *weights,
                      int batch_rows, int input_width, int output_width,
                      int uses, float *energies, void *raw_stream,
                      void *raw_blas_handle) {
    if (!x_batches || !weights || !energies || batch_rows <= 0 ||
        input_width <= 0 || output_width <= 0 || uses <= 0)
        return static_cast<int>(cudaErrorInvalidValue);

    const long long row_count = static_cast<long long>(batch_rows) * uses;
    if (row_count > INT_MAX)
        return static_cast<int>(cudaErrorInvalidValue);
    const int rows = static_cast<int>(row_count);
    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);
    const cublasHandle_t handle = static_cast<cublasHandle_t>(raw_blas_handle);

    // Preparing G costs K*M*K multiply-adds; applying it costs rows*K*K.
    // The direct route costs rows*K*M. Use the transformed route only when
    // this arithmetic model favors it, and only when cuBLAS is available.
    const bool use_gram = handle != nullptr && output_width > input_width &&
        static_cast<long long>(rows) * (output_width - input_width) >
        static_cast<long long>(input_width) * output_width;

    if (!use_gram) {
        direct_energy<<<rows, 256, 0, stream>>>(x_batches, weights, energies,
                                               rows, input_width, output_width);
        return static_cast<int>(cudaPeekAtLastError());
    }

    cublasHandle_t blas = handle;
    cudaStream_t old_stream = nullptr;
    cublasPointerMode_t old_pointer_mode = CUBLAS_POINTER_MODE_HOST;
    cublasStatus_t status = cublasGetStream(blas, &old_stream);
    if (status != CUBLAS_STATUS_SUCCESS) return cublas_error(status);
    status = cublasGetPointerMode(blas, &old_pointer_mode);
    if (status != CUBLAS_STATUS_SUCCESS) return cublas_error(status);
    status = cublasSetStream(blas, stream);
    if (status != CUBLAS_STATUS_SUCCESS) return cublas_error(status);
    status = cublasSetPointerMode(blas, CUBLAS_POINTER_MODE_HOST);
    if (status != CUBLAS_STATUS_SUCCESS) {
        cublasSetStream(blas, old_stream);
        return cublas_error(status);
    }

    const size_t gram_bytes = static_cast<size_t>(input_width) *
                              static_cast<size_t>(input_width) * sizeof(float);
    float *gram = nullptr;
    cudaError_t error = cudaMalloc(reinterpret_cast<void **>(&gram), gram_bytes);
    if (error != cudaSuccess) {
        cublasSetPointerMode(blas, old_pointer_mode);
        cublasSetStream(blas, old_stream);
        return static_cast<int>(error);
    }

    const float alpha = 1.0f;
    const float beta = 0.0f;
    // W is row-major [K,M], so its storage is column-major W^T [M,K].
    // W^T transposed times W^T produces the symmetric K-by-K Gram matrix.
    status = cublasSgemm(blas, CUBLAS_OP_T, CUBLAS_OP_N,
                         input_width, input_width, output_width,
                         &alpha, weights, output_width,
                         weights, output_width, &beta, gram, input_width);
    const cublasStatus_t pointer_restore =
        cublasSetPointerMode(blas, old_pointer_mode);
    const cublasStatus_t stream_restore = cublasSetStream(blas, old_stream);
    if (status != CUBLAS_STATUS_SUCCESS ||
        pointer_restore != CUBLAS_STATUS_SUCCESS ||
        stream_restore != CUBLAS_STATUS_SUCCESS) {
        cudaFree(gram);
        if (status != CUBLAS_STATUS_SUCCESS) return cublas_error(status);
        if (pointer_restore != CUBLAS_STATUS_SUCCESS)
            return cublas_error(pointer_restore);
        return cublas_error(stream_restore);
    }

    gram_energy<<<rows, 128, 0, stream>>>(x_batches, gram, energies, rows,
                                          input_width);
    error = cudaPeekAtLastError();
    const cudaError_t free_error = cudaFree(gram);
    if (error != cudaSuccess) return static_cast<int>(error);
    return static_cast<int>(free_error);
}
