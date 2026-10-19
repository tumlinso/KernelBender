# Composition: assign real subproblems to tensor microcircuits

**Use when:** an unfamiliar operation contains small bilinear subproblems and the consumer can keep a distributed result or reuse fixed coefficients. The transformation is to reinterpret the supported matrix products as a collection of local computational circuits, not to force every tensor-shaped value into a matrix instruction.

## Start from the equation and wiring

Write the exact bilinear subproblem as `Y=A*B`. Identify which indices are true independent rows/columns and which are contracted. Only after this map is explicit should a tile be chosen. One Atlas construction treats the documented SM70 explicit `m8n8k4` form as four independent `8×8×4` products executed by one full warp. This can represent four small state mixers, local graph-patch correlations or fixed basis transforms at once. The four products are a hardware decomposition for that documented form, not four arbitrary disjoint eight-lane subgroups. Use KernelWiki `hw-volta-mma`, `hw-volta-participation` and `hw-volta-numerics` for the exact form, ownership and numerical contracts.

For example, if a scientific operator consists of independent local linear transitions `y_j=A_j x_j`, place each real `A_j` in an independent subproblem. Do not take one coupled state vector and split it into four blocks unless the matrix is actually block diagonal or the missing cross-terms are computed elsewhere. A low-dimensional factorization can also be used when it is exact or when the caller permits its measured approximation; a convenient reshape does not prove such structure. (Atlas M24; C10.)

## Compose the ownership with the next operator

Write `P(x)=(lane,slot)` for the producer and `Q(x)=(lane,slot)` for the next consumer. If the producer's canonicalization and the consumer's retile are inverse maps, omit both and apply the middle operation in the retained coordinates. For an elementwise function and common permutation `p`, `p(f(x))=f(p(x))` if all per-element parameters use the same map. For reductions, confirm that axes and collective participants still match. Explicit PTX ownership is not a definition of raw WMMA fragment storage. See `hw-volta-atlas-e09-mma-coordinate`: the finite coordinate check validated the explicit form, while WMMA output checks did not establish its raw slot map.

Carry a useful fragment through a mask, elementwise transform, second local bilinear operator or a selected consumer. A four-lane set of Hadamard butterflies may be cheaper with shuffle/add; an all-ones row used once may be cheaper with a direct reduction. Tensor operation counts alone omit padding, operand creation, fragment exchange, conversion, accumulation and output extraction. The strongest comparison is the complete producer-to-observable-output chain. (Atlas M25, M27; C12, C13, C16, C36.)

## Numerical obligations

The composition must preserve both the real-valued equation and its required finite-precision behavior. Identify input quantization, accumulation type, reduction order, normalization, output conversion and repeated-use error growth. If an intermediate is rounded in the caller's original pipeline, algebraically moving a matrix product across it may change semantics. If using a high/low expansion, state the neglected residual and bound the actual component/accumulator error; if the caller only needs a predicate, a certified screen/refine chain may be a better fit. Retrieve `hw-volta-numerics` and the exact page for the actual target.

## Discriminating comparison

Retain the best library for regular dense work, a structured SIMT implementation for tiny transforms, and the uncompressed path required by the output. Validate a labeled/one-hot ownership map and finite-precision oracle before measuring. Then measure equal useful work including operand staging, packing, intermediate conversions, extra instructions, final extraction and any setup. Examine spills or generated code only to answer an identified routing question.

Reject the candidate if the mapping mixes semantically coupled inputs incorrectly, active lanes do not match the collective contract, the numeric result violates the caller's tolerance, or routing/live state costs more than the deleted materialization. An approximate but algebraically attractive form is not a substitute for a missing proof.

**Bounded evidence:** E09 validated explicit PTX raw coordinates only; it did not verify arbitrary WMMA ownership. E12's four independent Hadamard blocks ran at selected sizes and its timing was kernel-resident; it did not establish a general tensor win or a recurrent transform. See `hw-volta-atlas-e09-mma-coordinate` and `hw-volta-atlas-e12-independent-transform`.

Atlas IDs: M24–M28; C10, C12, C13, C15, C16, C36; E09, E10, E12. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
