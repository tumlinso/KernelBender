# Packed arithmetic and bilinear hardware

This family changes the arithmetic domain or the semantic meaning assigned to a supported dot product. Start with the operator and its error contract. A short instruction or tensor shape does not make an unrelated computation fit; KernelWiki supplies exact formats, target forms and numerical limits.

## Packed integer as a small exact circuit

If four byte values contribute to one bounded score, use the conceptual identity

```text
score = Σ(i=0..3) x[i] * w[i]
```

to compare a packed dot path with scalar multiply-adds, packed comparisons, or Boolean logic. Prove signedness and an accumulator bound such as `|bias| + Σ|x[i]*w[i]| <= accumulator_max` for every valid input. Include packing and output conversion. The packed dot collapses products into a sum; it does not return each product independently. For the exact SM70 `dp4a` signed/unsigned forms and eligibility, retrieve `hw-volta-integer-routing`; it is a packed scalar dot, not integer Tensor Core MMA. For binary overlap, word AND plus population count is a stronger starting point than numeric expansion. (Atlas M08, M09; C08, C11.)

Bounded positional encodings offer another construction. Let `B=2^g`, `A=Σ a_i B^i`, and `D=Σ d_j B^j`. Then the ordinary integer product has polynomial coefficients `c_k=Σ_{i+j=k}a_i d_j`. The encoding is exact only if every `c_k < B`, the complete product fits, and extraction uses correct masks. For four digits each at most three, `c_k<=36`, so `g=6` provides guard space. This is a candidate for a fixed small convolution, not carryless multiplication. Count input packing, 64-bit multiplication and all extraction; signed inputs need their own proof. (Atlas M09, M11; C07.)

An exact-integer problem can sometimes be converted to binary64 for several operations, but requiring each input to be representable is insufficient. Every product and intermediate sum must remain exact, and conversions, register use and dependency depth belong in the comparison. A mixed numerical form can also split `A=Ah+Al` and `B=Bh+Bl`, retaining `AhBh+AhBl+AlBh` and bounding the omitted `AlBl` term only after choosing a norm, scales and actual input/accumulation errors. These are mathematical options, not promised Volta throughput paths. (Atlas M10, M11, M28; C09, C15.)

## A tensor instruction as a local bilinear circuit

For a true bilinear operation, write `Y=A*B` and assign semantic rows, columns and reduction coordinates before choosing a supported tile. On the documented SM70 explicit PTX form, the Atlas interprets one full-warp collective as four independent `8×8×4` products. That can map a few local transforms or state mixers into one instruction, but only if those are the real independent products. The mathematical decomposition and its numerical appropriateness are design questions; exact lane/slot ownership, instruction syntax and participant scope belong to KernelWiki pages `hw-volta-mma`, `hw-volta-participation` and `hw-volta-numerics`.

Examples worth comparing include four graph-patch correlations, a small basis change, independent local linear state updates and common-neighbor counts. For binary incidence matrices `X` and `Y`, `C = X Yᵀ` gives pairwise intersections because multiplication is AND and addition counts. If the consumer wants a threshold mask rather than every `C[i,j]`, route toward that observable and compare packed AND+POPC before expanding into half values. If the operator is a 4×4 Hadamard block, its shuffle/add butterfly is the natural strong baseline; padding it into a dense product may do unnecessary work. (Atlas M24, M26, M27; C10–C13.)

Map accumulator ownership through the next operator. If the output's distributed coordinates are directly useful, a fragment-native producer/consumer chain may remove a store, reload and transpose. Do not infer that raw WMMA fragment storage has the explicit PTX map. Include operand construction, padding, conversions, routing, accumulation semantics, final extraction and live-fragment pressure. Exact volume and supported format must be taken from KernelWiki for the target, never copied from a neighboring generation. (Atlas M25; C16, C36.)

## Screening and nonlinear forms

Approximation is particularly useful when the required output is a decision and most values are far from its boundary. Given `|s - ŝ| <= ε`, an exact predicate `s >= τ` can accept when `ŝ-ε >= τ`, reject when `ŝ+ε < τ`, and refine all other cases. The proof must bound the actual input conversion, operator, table/interpolation or accumulation and output extraction. An observed maximum error is not such a proof. Route ambiguous items with a mask and compare all bound, queue and exact-fallback costs with direct exact evaluation. If near-boundary cases are common, the extra stage may only add work. (Atlas M10, M23, M28; C14, C31.)

## Decision checks

Keep direct integer/native arithmetic, structured SIMT, the best applicable library and packed bitset methods in the comparison. Check input ranges, signedness, overflow, FP exceptional values, rounding changes, and repeated accumulation. Separate the exact mathematical identity from the finite-precision operator promised by the caller. A successful CPU identity or small GPU corpus cannot guarantee all tensor rounding or threshold decisions.

Falsify cheaply before timing: exhaustive small domains for packed Boolean or guard-digit formulas; adversarial max-range and cancellation tests for numeric encodings; labeled coordinates for ownership; then legal compile and generated-code inspection only when it answers a concrete mapping question. Time the complete useful region, including setup/reuse when paid. For a conventional large dense GEMM, cuBLAS/cuBLASLt is the default control. Custom microcircuits need a real structural advantage, such as small fixed dimensions, fused downstream use, or an output projection unavailable from a materialized matrix result.

**Bounded evidence:** E09 validated explicit PTX coordinates for one form, not WMMA raw ownership; E11 found packed intersection lowest for one dense 16×16 matrix and ran actual iteration count one; E12 covered four independent 4-variable Hadamard blocks and did not test `M^r x`; E39 found native integer arithmetic generally led the tested full-adder cells, with no bitplane crossover established. Retrieve the corresponding E09, E11, E12 and E39 rows listed in [KernelWiki contracts](../wiki-contracts.md) before relying on these comparisons.

Atlas IDs: M08–M11, M23–M28; C07–C15, C31, C36; E09–E13, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
