#include "candidate_api.h"

#include <cuda_runtime.h>
#include <stddef.h>
#include <stdint.h>

namespace {
constexpr int kThreads = 256;
constexpr int kTile = 1024;
constexpr int kMaxTiledSteps = 128;

__device__ __forceinline__ unsigned int reduce_block_count(
    unsigned int local_count, uint32_t *count, unsigned int *partial) {
    const unsigned int tid = threadIdx.x;
    partial[tid] = local_count;
    __syncthreads();
    for (unsigned int stride = kThreads / 2; stride != 0; stride >>= 1) {
        if (tid < stride) partial[tid] += partial[tid + stride];
        __syncthreads();
    }
    if (tid == 0) {
        if (gridDim.x == 1) {
            *count = partial[0];
        } else {
            atomicAdd(reinterpret_cast<unsigned int *>(count), partial[0]);
        }
    }
    return partial[0];
}

__global__ void transition_one_step(const uint8_t *src, const uint8_t *mask,
                                    const uint8_t *rule, int n,
                                    uint8_t *dst, uint32_t *count) {
    __shared__ unsigned int partial[kThreads];
    const unsigned int tid = threadIdx.x;
    const int base = static_cast<int>(blockIdx.x) * kTile;
    const int span = (n - base < kTile) ? n - base : kTile;
    unsigned int local_count = 0;
    for (int offset = static_cast<int>(tid); offset < span; offset += kThreads) {
        const int i = base + offset;
        const int left = (i == 0) ? n - 1 : i - 1;
        const unsigned int index =
            (static_cast<unsigned int>(src[i]) * 4u + src[left]) * 2u + mask[i];
        const uint8_t value = rule[index];
        dst[i] = value;
        local_count += static_cast<unsigned int>(value == 3);
    }
    reduce_block_count(local_count, count, partial);
}

__global__ void transition_tiled_epoch(const uint8_t *initial_state,
                                       const uint8_t *mask,
                                       const uint8_t *rule, int n, int steps,
                                       uint8_t *final_state,
                                       uint32_t *count) {
    __shared__ unsigned int partial[kThreads];
    extern __shared__ uint8_t storage[];

    const int base = static_cast<int>(blockIdx.x) * kTile;
    const int output_count = (n - base < kTile) ? n - base : kTile;
    const int span = output_count + steps;
    uint8_t *current = storage;
    uint8_t *next = current + span;
    uint8_t *local_mask = next + span;

    for (int j = static_cast<int>(threadIdx.x); j < span; j += kThreads) {
        long long global = static_cast<long long>(base) + j - steps;
        global %= n;
        if (global < 0) global += n;
        const int source = static_cast<int>(global);
        current[j] = initial_state[source];
        local_mask[j] = mask[source];
    }
    __syncthreads();

    for (int step = 1; step <= steps; ++step) {
        for (int j = step + static_cast<int>(threadIdx.x); j < span;
             j += kThreads) {
            const unsigned int index =
                (static_cast<unsigned int>(current[j]) * 4u + current[j - 1]) * 2u +
                local_mask[j];
            next[j] = rule[index];
        }
        __syncthreads();
        uint8_t *swap = current;
        current = next;
        next = swap;
    }

    unsigned int local_count = 0;
    for (int offset = static_cast<int>(threadIdx.x); offset < output_count;
         offset += kThreads) {
        const uint8_t value = current[steps + offset];
        final_state[base + offset] = value;
        local_count += static_cast<unsigned int>(value == 3);
    }
    reduce_block_count(local_count, count, partial);
}

__global__ void transition_scalar(const uint8_t *src, const uint8_t *mask,
                                  const uint8_t *rule, int n, uint8_t *dst) {
    const size_t i = static_cast<size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    if (i < static_cast<size_t>(n)) {
        const int site = static_cast<int>(i);
        const int left = (site == 0) ? n - 1 : site - 1;
        const unsigned int index =
            (static_cast<unsigned int>(src[site]) * 4u + src[left]) * 2u + mask[site];
        dst[site] = rule[index];
    }
}

__global__ void transition_scalar_and_count(const uint8_t *src,
                                            const uint8_t *mask,
                                            const uint8_t *rule, int n,
                                            uint8_t *dst, uint32_t *count) {
    __shared__ unsigned int partial[kThreads];
    const size_t i = static_cast<size_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    unsigned int local_count = 0;
    if (i < static_cast<size_t>(n)) {
        const int site = static_cast<int>(i);
        const int left = (site == 0) ? n - 1 : site - 1;
        const unsigned int index =
            (static_cast<unsigned int>(src[site]) * 4u + src[left]) * 2u + mask[site];
        const uint8_t value = rule[index];
        dst[site] = value;
        local_count = static_cast<unsigned int>(value == 3);
    }
    reduce_block_count(local_count, count, partial);
}

int fallback_epoch(const uint8_t *initial_state, const uint8_t *mask,
                   const uint8_t *rule, int n, int steps,
                   uint8_t *final_state, uint32_t *count,
                   cudaStream_t stream) {
    uint8_t *scratch_a = nullptr;
    uint8_t *scratch_b = nullptr;
    cudaError_t error = cudaMalloc(reinterpret_cast<void **>(&scratch_a),
                                   static_cast<size_t>(n));
    if (error != cudaSuccess) return static_cast<int>(error);
    error = cudaMalloc(reinterpret_cast<void **>(&scratch_b),
                       static_cast<size_t>(n));
    if (error != cudaSuccess) {
        cudaFree(scratch_a);
        return static_cast<int>(error);
    }

    error = cudaMemsetAsync(count, 0, sizeof(uint32_t), stream);
    const int blocks = (n - 1) / kThreads + 1;
    const uint8_t *src = initial_state;
    for (int step = 0; error == cudaSuccess && step < steps; ++step) {
        const bool last = step == steps - 1;
        uint8_t *dst = final_state;
        if (!last) {
            dst = (src == initial_state || src == scratch_b) ? scratch_a : scratch_b;
        }
        if (last) {
            transition_scalar_and_count<<<blocks, kThreads, 0, stream>>>(
                src, mask, rule, n, dst, count);
        } else {
            transition_scalar<<<blocks, kThreads, 0, stream>>>(src, mask, rule, n, dst);
        }
        error = cudaPeekAtLastError();
        src = dst;
    }

    const cudaError_t free_b = cudaFree(scratch_b);
    const cudaError_t free_a = cudaFree(scratch_a);
    if (error != cudaSuccess) return static_cast<int>(error);
    if (free_b != cudaSuccess) return static_cast<int>(free_b);
    return static_cast<int>(free_a);
}
}  // namespace

extern "C" int kb_run(const uint8_t *initial_state, const uint8_t *mask,
                      const uint8_t *rule, int n, int steps,
                      uint8_t *final_state, uint32_t *count_state_three,
                      void *raw_stream) {
    if (!initial_state || !mask || !rule || !final_state || !count_state_three ||
        n <= 0 || steps <= 0) {
        return static_cast<int>(cudaErrorInvalidValue);
    }
    const cudaStream_t stream = reinterpret_cast<cudaStream_t>(raw_stream);

    if (steps == 1) {
        const int blocks = (n - 1) / kTile + 1;
        cudaError_t error = cudaSuccess;
        if (blocks > 1) {
            error = cudaMemsetAsync(count_state_three, 0, sizeof(uint32_t), stream);
        }
        if (error != cudaSuccess) return static_cast<int>(error);
        transition_one_step<<<blocks, kThreads, 0, stream>>>(
            initial_state, mask, rule, n, final_state, count_state_three);
        return static_cast<int>(cudaPeekAtLastError());
    }

    if (steps <= kMaxTiledSteps) {
        const int tile = (n < kTile) ? n : kTile;
        const int blocks = (n - 1) / tile + 1;
        cudaError_t error = cudaSuccess;
        if (blocks > 1) {
            error = cudaMemsetAsync(count_state_three, 0, sizeof(uint32_t), stream);
        }
        if (error != cudaSuccess) return static_cast<int>(error);
        const size_t shared_bytes =
            3u * (static_cast<size_t>(tile) + static_cast<size_t>(steps));
        transition_tiled_epoch<<<blocks, kThreads, shared_bytes, stream>>>(
            initial_state, mask, rule, n, steps, final_state, count_state_three);
        return static_cast<int>(cudaPeekAtLastError());
    }

    return fallback_epoch(initial_state, mask, rule, n, steps, final_state,
                          count_state_three, stream);
}
