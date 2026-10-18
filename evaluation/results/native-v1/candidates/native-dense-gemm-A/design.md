# Native dense GEMM control design

## Contract
Compute row-major FP32 C = alpha*A*B + beta*C for all output elements, for arbitrary finite represented FP32 values. The CPU reference accumulates in binary64 over those represented values. Admission tolerance is abs(error) <= 2e-5 + 5e-5*abs(reference). The fixed cases are 512x512x512 with alpha=1 and beta=0, and 1024x384x256 with alpha=0.75 and beta=0.25. The caller supplies device buffers, a stream, and a cuBLAS handle.

## Selected route
Retain the provided cuBLAS SGEMM implementation. This is regular dense GEMM, the operation cuBLAS owns directly, and both tested cases have standard dimensions. The implementation maps row-major C=A*B to column-major C-transpose=B-transpose*A-transpose by swapping A and B and passing dimensions n,m,k. It sets the caller stream on the supplied handle before submitting the operation. SGEMM evaluates both alpha and beta and writes the complete output.

## Rejected custom route
A custom tile would duplicate a mature dense matrix multiply path and add code, launch, and numerical behavior choices without an available measurement showing that those costs are recovered. The required tolerance is adequate for the baseline design, but runtime correctness was not executable in this isolated namespace. No custom precision or output shortcut is justified.

## Evidence and limits
The source was retained byte-for-byte from the supplied baseline. The provided compile harness succeeded once for sm_70. No CUDA runtime, device execution, oracle comparison, sanitizer, or timing was available. Therefore this artifact is a compiled candidate and design control, not a runtime-validated or measured speedup.
