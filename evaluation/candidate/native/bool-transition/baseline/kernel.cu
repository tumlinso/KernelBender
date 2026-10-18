#include "candidate_api.h"

#include <cuda_runtime.h>

namespace {
__global__ void transition(const uint8_t *src, const uint8_t *mask,
                           const uint8_t *rule, uint8_t *dst, int n) {
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        const int left = (i == 0) ? n - 1 : i - 1;
        const int index = (static_cast<int>(src[i]) * 4 + src[left]) * 2 + mask[i];
        dst[i] = rule[index];
    }
}

__global__ void count_three(const uint8_t *state, int n, uint32_t *count) {
    __shared__ unsigned block_count;
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (threadIdx.x == 0) block_count = 0;
    __syncthreads();
    const bool selected = i < n && state[i] == 3;
    const unsigned warp = __ballot_sync(0xffffffffu, selected);
    if ((threadIdx.x & 31) == 0) atomicAdd(&block_count, static_cast<unsigned>(__popc(warp)));
    __syncthreads();
    if (threadIdx.x == 0) atomicAdd(count, block_count);
}
}  // namespace

extern "C" int kb_run(const uint8_t *initial_state, const uint8_t *mask,
                      const uint8_t *rule, int n, int steps,
                      uint8_t *final_state, uint32_t *count_state_three,
                      void *raw_stream) {
    if (!initial_state || !mask || !rule || !final_state || !count_state_three || n <= 0 || steps <= 0)
        return static_cast<int>(cudaErrorInvalidValue);
    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);
    uint8_t *scratch_a = nullptr;
    uint8_t *scratch_b = nullptr;
    cudaError_t error = cudaMalloc(&scratch_a, static_cast<size_t>(n));
    if (error != cudaSuccess) return static_cast<int>(error);
    error = cudaMalloc(&scratch_b, static_cast<size_t>(n));
    if (error != cudaSuccess) {
        cudaFree(scratch_a);
        return static_cast<int>(error);
    }

    const int blocks = (n + 255) / 256;
    const uint8_t *src = initial_state;
    uint8_t *dst = scratch_a;
    for (int step = 0; step < steps; ++step) {
        if (step == steps - 1) dst = final_state;
        transition<<<blocks, 256, 0, stream>>>(src, mask, rule, dst, n);
        error = cudaPeekAtLastError();
        if (error != cudaSuccess) break;
        src = dst;
        dst = (dst == scratch_a) ? scratch_b : scratch_a;
    }
    if (error == cudaSuccess) error = cudaMemsetAsync(count_state_three, 0, sizeof(uint32_t), stream);
    if (error == cudaSuccess) {
        count_three<<<blocks, 256, 0, stream>>>(final_state, n, count_state_three);
        error = cudaPeekAtLastError();
    }
    cudaError_t free_b = cudaFree(scratch_b);
    cudaError_t free_a = cudaFree(scratch_a);
    if (error != cudaSuccess) return static_cast<int>(error);
    if (free_b != cudaSuccess) return static_cast<int>(free_b);
    return static_cast<int>(free_a);
}
