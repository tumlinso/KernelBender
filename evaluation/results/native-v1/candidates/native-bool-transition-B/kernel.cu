#include "candidate_api.h"

#include <cuda_runtime.h>
#include <stddef.h>
#include <stdint.h>

namespace {
constexpr int kThreads = 256;
constexpr int kTile = 256;
constexpr size_t kSharedLimit = 40u * 1024u;

__global__ void small_epoch(const uint8_t *initial_state, const uint8_t *mask,
                            const uint8_t *rule, int n, int steps,
                            uint8_t *final_state, uint32_t *count) {
    extern __shared__ uint8_t storage[];
    uint8_t *a = storage;
    uint8_t *b = a + n;
    uint8_t *smask = b + n;
    uint8_t *srule = smask + n;
    __shared__ unsigned sums[kThreads];

    const int tid = threadIdx.x;
    for (int i = tid; i < n; i += blockDim.x) {
        a[i] = initial_state[i];
        smask[i] = mask[i];
    }
    for (int i = tid; i < 32; i += blockDim.x) srule[i] = rule[i];
    __syncthreads();

    uint8_t *src = a;
    uint8_t *dst = b;
    for (int step = 0; step < steps; ++step) {
        for (int i = tid; i < n; i += blockDim.x) {
            const int left = (i == 0) ? n - 1 : i - 1;
            const int index = (static_cast<int>(src[i]) * 4 +
                               static_cast<int>(src[left])) * 2 + smask[i];
            dst[i] = srule[index];
        }
        __syncthreads();
        uint8_t *tmp = src;
        src = dst;
        dst = tmp;
    }

    unsigned local = 0;
    for (int i = tid; i < n; i += blockDim.x) {
        const uint8_t value = src[i];
        final_state[i] = value;
        local += static_cast<unsigned>(value == 3);
    }
    sums[tid] = local;
    __syncthreads();
    for (int stride = kThreads / 2; stride != 0; stride >>= 1) {
        if (tid < stride) sums[tid] += sums[tid + stride];
        __syncthreads();
    }
    if (tid == 0) *count = sums[0];
}

__global__ void fused_tiles(const uint8_t *initial_state, const uint8_t *mask,
                            const uint8_t *rule, int n, int steps,
                            uint8_t *final_state, uint32_t *count) {
    extern __shared__ uint8_t storage[];
    const int length = kTile + steps;
    uint8_t *a = storage;
    uint8_t *b = a + length;
    uint8_t *smask = b + length;
    uint8_t *srule = smask + length;
    __shared__ unsigned sums[kThreads];

    const int tid = threadIdx.x;
    const int base = blockIdx.x * kTile;
    for (int j = tid; j < length; j += blockDim.x) {
        const long long global = static_cast<long long>(base) + j - steps;
        int wrapped = static_cast<int>(global % n);
        if (wrapped < 0) wrapped += n;
        a[j] = initial_state[wrapped];
        smask[j] = mask[wrapped];
    }
    for (int i = tid; i < 32; i += blockDim.x) srule[i] = rule[i];
    __syncthreads();

    uint8_t *src = a;
    uint8_t *dst = b;
    for (int step = 0; step < steps; ++step) {
        for (int j = tid; j < length; j += blockDim.x) {
            if (j > step) {
                const int index = (static_cast<int>(src[j]) * 4 +
                                   static_cast<int>(src[j - 1])) * 2 + smask[j];
                dst[j] = srule[index];
            }
        }
        __syncthreads();
        uint8_t *tmp = src;
        src = dst;
        dst = tmp;
    }

    const int output_count = (n - base < kTile) ? n - base : kTile;
    unsigned local = 0;
    for (int k = tid; k < output_count; k += blockDim.x) {
        const uint8_t value = src[steps + k];
        final_state[base + k] = value;
        local += static_cast<unsigned>(value == 3);
    }
    sums[tid] = local;
    __syncthreads();
    for (int stride = kThreads / 2; stride != 0; stride >>= 1) {
        if (tid < stride) sums[tid] += sums[tid + stride];
        __syncthreads();
    }
    if (tid == 0 && sums[0] != 0) atomicAdd(count, sums[0]);
}

__global__ void transition(const uint8_t *src, const uint8_t *mask,
                           const uint8_t *rule, uint8_t *dst, int n) {
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        const int left = (i == 0) ? n - 1 : i - 1;
        const int index = (static_cast<int>(src[i]) * 4 +
                           static_cast<int>(src[left])) * 2 + mask[i];
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
    if ((threadIdx.x & 31) == 0)
        atomicAdd(&block_count, static_cast<unsigned>(__popc(warp)));
    __syncthreads();
    if (threadIdx.x == 0) atomicAdd(count, block_count);
}
}  // namespace

extern "C" int kb_run(const uint8_t *initial_state, const uint8_t *mask,
                      const uint8_t *rule, int n, int steps,
                      uint8_t *final_state, uint32_t *count_state_three,
                      void *raw_stream) {
    if (!initial_state || !mask || !rule || !final_state ||
        !count_state_three || n <= 0 || steps <= 0)
        return static_cast<int>(cudaErrorInvalidValue);

    const cudaStream_t stream = static_cast<cudaStream_t>(raw_stream);
    if (n <= 1024) {
        const size_t shared_bytes = 3u * static_cast<size_t>(n) + 32u;
        small_epoch<<<1, kThreads, shared_bytes, stream>>>(
            initial_state, mask, rule, n, steps, final_state,
            count_state_three);
        return static_cast<int>(cudaPeekAtLastError());
    }

    const size_t fused_length = static_cast<size_t>(kTile) +
                                static_cast<size_t>(steps);
    const size_t fused_shared = 3u * fused_length + 32u;
    if (fused_shared <= kSharedLimit) {
        cudaError_t error =
            cudaMemsetAsync(count_state_three, 0, sizeof(uint32_t), stream);
        if (error != cudaSuccess) return static_cast<int>(error);
        const int blocks = (n - 1) / kTile + 1;
        fused_tiles<<<blocks, kThreads, fused_shared, stream>>>(
            initial_state, mask, rule, n, steps, final_state,
            count_state_three);
        return static_cast<int>(cudaPeekAtLastError());
    }

    uint8_t *scratch_a = nullptr;
    uint8_t *scratch_b = nullptr;
    cudaError_t error = cudaMalloc(&scratch_a, static_cast<size_t>(n));
    if (error != cudaSuccess) return static_cast<int>(error);
    error = cudaMalloc(&scratch_b, static_cast<size_t>(n));
    if (error != cudaSuccess) {
        cudaFree(scratch_a);
        return static_cast<int>(error);
    }

    const int blocks = (n - 1) / kThreads + 1;
    const uint8_t *src = initial_state;
    uint8_t *dst = scratch_a;
    for (int step = 0; step < steps; ++step) {
        if (step == steps - 1) dst = final_state;
        transition<<<blocks, kThreads, 0, stream>>>(src, mask, rule, dst, n);
        error = cudaPeekAtLastError();
        if (error != cudaSuccess) break;
        src = dst;
        dst = (dst == scratch_a) ? scratch_b : scratch_a;
    }
    if (error == cudaSuccess)
        error = cudaMemsetAsync(count_state_three, 0, sizeof(uint32_t), stream);
    if (error == cudaSuccess) {
        count_three<<<blocks, kThreads, 0, stream>>>(
            final_state, n, count_state_three);
        error = cudaPeekAtLastError();
    }
    const cudaError_t free_b = cudaFree(scratch_b);
    const cudaError_t free_a = cudaFree(scratch_a);
    if (error != cudaSuccess) return static_cast<int>(error);
    if (free_b != cudaSuccess) return static_cast<int>(free_b);
    return static_cast<int>(free_a);
}
