# Blind design fixtures: Atlas consolidation

These cases were authored from the consolidation acceptance criteria before
reading the expanded KernelBender references or any private intended answers.
They specify workloads and observable results, not candidate designs. Use them
to probe retrieval and reasoning; they are not GPU benchmarks.

For each case, record (1) the first KernelBender entry points opened, (2) the
concrete design brief produced, (3) the strongest baseline, (4) exact
KernelWiki pages and architecture-filtered query used for factual constraints,
(5) a falsifiable experiment, and (6) claims that remain unverified. Keep
retrieval logs so load size and routes can be inspected.

## B1 — Independent threshold updates on small graphs

**Need.** For each of 128 independent directed graphs with 64 vertices, update
binary vertex states synchronously by

`x'[v] = 1 iff (sum over u in In(v) of x[u]) >= 2`.

Input is CSR (`offsets[65]`, `indices[E]`) and one 64-bit state word per graph.
Self-edges are permitted; duplicate edges are not. Graphs may have isolated
vertices or in-degree 0/1. Return one 64-bit state word per graph. The old state
must be used for every vertex in the update. Exact Boolean output is required.

**Target.** V100 / SM70. No persistent graph preprocessing is required for one
call. Report a baseline appropriate for this small workload and the dimensions
that would make an alternative worthwhile.

**Boundary probes.** In-degree 0, 1, 2, 63; all-zero and all-one states; vertex
63; and a graph where an in-place sequential update differs from the required
synchronous result.

## B2 — Repeated composed query over a fixed sparse operator

**Need.** A fixed directed sparse matrix `A` has shape `4096 x 4096`, exactly
32 unique destinations per row, and nonnegative integer weights in `[1, 7]`.
For each of 512 query batches, receive `Q` as 64 binary vectors of length 4096.
For every query row `q`, produce a binary output

`y[q, i] = 1 iff sum_j A[i,j] * q[j] >= tau[i]`,

where `tau` is a fixed positive per-row threshold supplied with `A`. The same
`A` and `tau` are reused across all batches; query data changes each batch.
Results must be exact. The application consumes only `y`, not the weighted
intermediate. Initialization/preparation time and storage must be included in
the repeated-use break-even discussion.

**Target.** V100 / SM70. Compare a conventional sparse multiply-plus-threshold
path with a concrete composed alternative. State the reuse count at which any
preparation could amortize, and propose one small experiment that can reject
the alternative. Do not claim a speedup without execution evidence.

**Boundary probes.** `tau[i]` equal to 1, exact maximum row sum, one above the
maximum; all-zero/all-one query rows; one query versus all 512 batches; and
include preprocessing, storage, launches and output materialization in costs.

## B3 — Block operator with a consumer-owned output layout

**Need.** Each sample contains a `4 x 4` FP16 matrix `A` and `4 x 4` FP16
matrix `B`. Compute `C = A B` with FP32 accumulation and round each result
once to FP16. The next stage consumes `C` in a fixed lane/slot ownership map.
Group samples in fours per warp. For group `g` and local sample index
`s ∈ {0,1,2,3}`, global sample index is `4*g+s`. Let `p = 4*j + i`; the
owner of `C[i,j]` is
`(lane=(p+16*(s mod 2)) mod 32, slot=floor(s/2))`. It performs an elementwise
operation there and does not require row-major storage. There are 1,000,000
independent samples. The numerical contract is maximum absolute
error `<= 0.02` against FP64 multiplication of the FP16 inputs, with inputs
bounded to `[-2,2]`.

**Target.** V100 / SM70. Explain whether an architecture-specific tensor
operation can help, what ownership contract must be established for the exact
instruction/API form, and whether the downstream ownership can be retained
without a conversion. Keep measured facts separate from a proposed mapping.

**Boundary probes.** Check output coordinates in all four quadrants and the
ownership map's slot calculation. Do not infer opaque WMMA fragment ownership
from an explicit-PTX mapping.

## B4 — Conventional dense-library control

**Need.** Compute contiguous row-major `C = A B` for FP16 matrices
`A[8192,4096]`, `B[4096,8192]`, FP32 accumulation, FP16 output. There is one
call, no reuse, no fused consumer, and no unusual sparsity or alignment beyond
the stated contiguous layout. Maximum absolute error is `0.1` against an
FP64 reference on a scaled random sample.

**Target.** H100 / SM90. Identify the ordinary baseline and why a speculative
custom representation should or should not be pursued before measuring it.
This is a negative control for gratuitous circuit invention.

## B5 — Unsupported mechanism on the requested target

**Need.** Stage two 128-byte tiles per block from global to shared memory,
overlap transfer of tile `k+1` with computation on tile `k`, then reduce each
tile to an FP32 sum. Each block owns 64 consecutive tiles. The reduction must
be deterministic for a fixed build and target. A portable fallback is
acceptable if the requested overlap mechanism is unavailable.

**Target.** V100 / SM70, CUDA C++ device code. State whether the newer
asynchronous global-to-shared copy / pipeline facility described by the
request can be used here. Retrieve the exact architecture boundary and give a
valid fallback path. Do not silently substitute driver-only mechanisms.

**Boundary probes.** Distinguish PTX/toolkit syntax exposure from native SM70
support. Keep synchronization and memory visibility requirements explicit.

## Blind evaluation record

Do not use this section to store a preferred implementation in advance. After
each run, append:

- date and exact KernelBender / KernelWiki commits;
- prompt shown to the design agent;
- files opened and query commands/results;
- produced brief and cited page IDs;
- factual or arithmetic checks run;
- pass/fail per acceptance criterion, with evidence;
- capability and scope limits.

Passing these authored fixtures demonstrates only that these task statements
are well-formed and that the tested agent could retrieve and reason about the
covered material. It does not establish agent efficacy generally, GPU
correctness, performance, or replacement completeness.
