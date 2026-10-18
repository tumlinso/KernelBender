# E06 — Keep the strong conventional route when it fits

Compute row-major FP32 `C = 0.75*A*B + 0.25*C` for arbitrary finite dense
inputs, with `A[512,768]`, `B[768,256]`, and `C[512,256]`. Every output is
required. The caller permits ordinary FP32 accumulation and requires
`atol=2e-5, rtol=2e-5` against an independent FP64 reference. There is no
reusable sparsity, fixed input data, or permission to change the operation.
A verified cuBLAS SGEMM implementation is already available.

Give the recommendation for a normal implementation request, then describe
what extra structural question an explicit request to reconsider the
formulation would justify. Do not invent sparsity, relax precision, or propose
custom code solely to appear novel. Record the design and implementation
effort the conventional choice avoids.
