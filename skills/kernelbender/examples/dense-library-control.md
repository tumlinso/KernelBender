# Example: keep a regular dense operation on its library route

**Status:** conventional negative control; no local measurement.

Suppose the caller asks for a large dense `C=A*B`, the dtype and layout match an established CUDA library path, and the complete output is observable. There is no fixed low-rank structure, reuse boundary, unusual output predicate or downstream fusion opportunity in the task. Keep cuBLAS/cuBLASLt as the baseline and first implementation. Check the exact dimensions, algorithm, workspace and numerical mode; a custom kernel must compare against the best eligible library call.

KernelBender becomes useful only if a real structural change appears—for example, only a small projection of `C` is observed, `B` stays fixed across enough calls to amortize `A`-independent preparation, or producer/consumer layouts can remove work while preserving the finite-precision contract. A different tile size or the desire to use a tensor mechanism is not by itself a new computation.

This is a negative control for the opportunity index: it must route away from its unusual mechanisms when they cannot remove caller-visible work. If a custom path is proposed, first state which library work or boundary it removes and what full-path test could disprove that premise. Sources: [CUDA-MAD], [CUDA-ROOT].
