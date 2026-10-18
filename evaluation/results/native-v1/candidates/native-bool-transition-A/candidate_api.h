#pragma once

#include <stdint.h>

// All pointers address device memory. `stream` is a caller-owned CUDA stream.
// Return zero on success; return a nonzero CUDA/runtime error otherwise.
extern "C" int kb_run(
    const uint8_t *initial_state,
    const uint8_t *mask,
    const uint8_t *rule,
    int n,
    int steps,
    uint8_t *final_state,
    uint32_t *count_state_three,
    void *stream);
