#pragma once

// All matrix/output pointers address device memory. `stream` is a caller-owned
// CUDA stream. `blas_handle` is a caller-created cuBLAS handle or null.
// Return zero on success; return a nonzero CUDA/runtime/library error otherwise.
extern "C" int kb_run(
    const float *x_batches,
    const float *weights,
    int batch_rows,
    int input_width,
    int output_width,
    int uses,
    float *energies,
    void *stream,
    void *blas_handle);
