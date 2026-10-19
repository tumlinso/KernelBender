# Composition: keep discrete state as a circuit

**Use when:** many independent instances follow the same small categorical transition, the consumer can use masks/planes, and state can stay encoded through more than one step. The construction applies to finite local rules, support propagation, selected graph patches and per-position count thresholds. It is not a universal replacement for scalar state or a dependent arithmetic recurrence.

## Construction

For a state variable with two bits at every logical position `i`, form bitplanes `p0[i]` and `p1[i]`. A rule with two input state bits and an eligibility mask is a Boolean function at each position. For a fixed rule, evaluate it plane-wise and leave the outputs as planes. With bit-sliced full-adder stages, independent bits can accumulate counts without a scalar counter per position:

```text
s0 = a XOR b XOR c
s1 = majority(a,b,c)       # a+b+c = s0 + 2*s1 at every position
```

For a threshold of at least two among three inputs, `majority(a,b,c)` is exactly the output mask. For more inputs, repeatedly reduce three equal-weight planes into sum/carry planes, preserving each bit's weight; compare the final weighted representation with the threshold without decoding every count. Shifts or lane exchanges implement neighbor relationships. A resulting active/support mask can feed another state transition directly, and rank/select is needed only if an output boundary requires compact external indices. (Atlas M01, M02, M06; C00, C02, C06, C37.)

A four-symbol sequence has another small exact mapping: encode symbols with two bitplanes `x0,x1`; equality against `y0,y1` is `~((x0 XOR y0) OR (x1 XOR y1)) & valid`. Window shifts need explicit cross-word carry or owner exchange. Add an additional plane or explicit rule for ambiguous symbols; do not merge them into an existing category without changing the semantics. This is a membership/equality circuit, not a general alignment/edit-distance algorithm. (Atlas M03, M06; C01.)

A small graph tile can use the same idea. If a tile has `n` vertices and stable adjacency masks `N(v)`, frontier step `F' = OR_{v in F} N(v)` is a mask union; visited suppression is `F' = F' & ~visited`. For multiple independent local updates, use bitplanes to hold each categorical field and combine membership/exclusion tests before materializing new IDs. This works when the tile's adjacency and bit/vertex mapping are known and neighboring tile crossings are few. It does not make a large irregular graph local: remote edges need a real communication path, and unbounded degree can dominate the word circuit. (Atlas M04, M06, M14; C05.)

## Representation and lifetime

Make the input permutation and validity mask explicit. Decide whether a lane owns an instance and word bits encode categories, or a lane owns a bitplane and another dimension supplies instances. The former gives many Boolean instances per word; the latter may reduce replication but requires routing among planes. Convert once, preserve the form across transitions, and extract only the caller-visible result. If the rule or adjacency changes, include update cost and invalidation. If every step immediately needs scalar state, encoding and decoding may dominate.

`cost(bitplanes) = encode + steps * (plane logic + neighbor exchange + state storage) + extract + updates`

Compare this with scalar/vector transitions, packed-byte comparisons, a well-structured CSR/bitmap implementation and any library relevant to the full task. Count word shifts, halo exchange, masks, padding, live planes, spills, output compaction and the reduced residency that state may cause. A bitplane does not compress arbitrary information; it rearranges it for repeated Boolean work.

## Correctness, baseline and experiment

Exhaustively compare small rule truth tables before running on a GPU. Include invalid tail bits, all-zero/all-one masks, threshold equalities, cross-word edges, empty frontier and topology changes. Check that every producer exchange has a participating source with a defined value. Use `hw-volta-participation` and `hw-volta-resources` for the exact target contract; use `hw-volta-feature-boundaries` before applying a newer-generation mechanism.

The smallest useful experiment compares equal semantic work over a cold conversion and several encoded steps, with output extraction included. Sweep transition count and topology/locality while holding the rule and outputs fixed. Reject the representation if the scalar/packed baseline is faster over the caller's horizon, exchange grows with the number of steps, or the expected reuse is broken by updates. This is a feasibility and cost test, not evidence of an application speedup.

**Evidence boundary:** Atlas E39 found native arithmetic generally led a selected repeated `uint32` full-adder workload; its small bitplane median ordering had an uncertainty interval crossing zero. That carry chain is a different semantic operator from parallel Boolean state or per-position thresholding. Atlas E11 found packed AND+POPC lowest for one dense 16×16 set-intersection output and actual iteration count one; it did not test the requested repeated-use horizon. Retrieve `hw-volta-atlas-e39-bitplane-addition` and `hw-volta-atlas-e11-packed-intersection` only as bounded comparisons, not family-wide decisions.

Atlas IDs: M01, M02, M04, M06, M14; C00, C02, C05, C06, C37; E01, E11, E13, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
