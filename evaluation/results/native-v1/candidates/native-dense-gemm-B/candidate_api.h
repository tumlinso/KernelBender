#pragma once

// A, B, and C are row-major device matrices; C is initialized on entry and
// must be fully overwritten with alpha*A*B + beta*C. `stream` is caller-owned
// and `blas_handle` is caller-created or null. Return zero on success.
extern "C" int kb_run(
    const float *a,
    const float *b,
    float *c,
    int m,
    int n,
    int k,
    float alpha,
    float beta,
    void *stream,
    void *blas_handle);
