# Composition: choose a domain for a bounded subproblem

**Use when:** a real workload has a short exact integer score, bounded convolution, threshold decision, or repeated query structure that may be evaluated more directly than its scalar floating-point reference. The idea is to choose an algebra and encoding whose operations match the desired result. It is not a license to change the operator or tolerance.

## Three distinct routes

**Packed dot for a short score.** For four bounded values, `s = bias + Σ x_i*w_i` can be represented as a packed integer dot when its signedness and accumulator range fit. The result is one score, not four products. Include input packing, scales/quantization and any final float conversion. The exact SM70 DP4A/DP2A formats, eligibility and accumulator signedness are in `hw-volta-integer-routing`. Keep an AND+POPC bitset method for pure binary intersections; it avoids expansion to numeric lanes. Compare both with the caller's strongest packed/vector library implementation. (Atlas M08–M09; C08, C11.)

**Guard-digit convolution.** If a small coefficient vector has nonnegative bounded digits, let `A=Σa_i B^i` and `D=Σd_i B^i`, with `B=2^g`. Their integer product contains the polynomial convolution coefficients as base-`B` digits only while each coefficient stays below `B` and the whole product fits. For four digits in `0..3`, `c_k<=36`; six guard bits per digit avoid coefficient carry. Shifts and masks extract results. Negative values, larger sizes and accumulator overflow require separate encodings; a clear CPU proof should include a counterexample with insufficient guard space. Count packing, wide multiply implementation and extraction against scalar multiply-add and packed-dot alternatives. (Atlas M09, M11; C07.)

**Bilinear tile or count.** For binary sets stored as incidence rows, `C=X Yᵀ` gives pairwise intersection counts. For a small fixed transform, a coefficient matrix computes the linear substep. These can fit a tensor operation only when their actual dimensions and numerical behavior fit the selected architecture. A threshold caller may need only `C>=t`, so consider screening or bitset output instead of materializing a dense matrix. Structured Hadamard, scan or prefix operators may have fewer useful terms in a shuffle/add circuit. (Atlas M24, M26–M28; C10–C14.)

## Error and observable contract

For each route, distinguish three layers:

1. The real/integer identity and its domain/range proof.
2. The target operation's finite-precision semantics, conversions, accumulation and extraction.
3. The caller's permitted result, including rounding points, ties, exceptional values and whether it needs every intermediate/output.

If approximate score `ŝ` has a proved bound `|s-ŝ|<=ε`, then `ŝ-ε>=τ` certifies accept and `ŝ+ε<τ` certifies reject for `s>=τ`; all other values need exact refinement. The bound must cover representation conversion and implementation behavior, not only the algebraic approximation. A finite random test or observed maximum cannot replace it. For exact bounded arithmetic, prove every product and partial sum, not just endpoint values. For repeated low/high correction, include error from all component products and accumulation order.

Use `hw-volta-numerics`, `hw-volta-feature-boundaries` and `hw-volta-mma` for exact Volta contract. For newer targets, use the exact architecture page; do not transfer tensor eligibility by analogy. [KernelWiki contracts](../wiki-contracts.md) lists those IDs.

## Economics and falsifier

Keep an ordinary integer or dense-library implementation as the control. Include packing/encoding, conversion, result materialization, query reuse and updates. If a dense answer matrix is not observable, do not reward an implementation for producing it quickly. If setup is reused, measure both cold epochs and the valid repeated-use horizon. An alternate arithmetic pipe only helps when it reduces the complete bottleneck instead of adding issue, registers, traffic or dependency pressure.

The first tests are small: exhaustive guard-digit cases including the first forbidden carry; signed and max-range accumulator tests; independent-oracle comparison for all threshold boundary values; then a complete-path shape where there is enough reuse to repay conversion. Reject on a violated range/error guarantee or if the strongest baseline already does less useful work.

**Evidence scope:** Atlas E11 only compared a dense 16×16 matrix of exact set intersections at three universes and actual iteration count one; packed AND+POPC was lowest in those cases. E12 compared one block-diagonal transform made from four independent 4-variable Hadamard blocks, not recurrent `M^r x`; resident timings excluded preparation/extraction. E39 compared selected repeated uint32 full-adder cells with full-path encode/decode/transfers but excluded allocations and lookup-table setup; native arithmetic generally led and no bitplane crossover was established. Fetch `hw-volta-atlas-e11-packed-intersection`, `hw-volta-atlas-e12-independent-transform` and `hw-volta-atlas-e39-bitplane-addition` for the source-backed boundaries.

Atlas IDs: M08–M11, M24, M26–M28; C07–C15, C31; E09–E13, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
