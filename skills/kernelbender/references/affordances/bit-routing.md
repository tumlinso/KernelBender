# Bit logic and positional routing

These mechanisms are useful when the natural object is a small set, local category, lane group or finite state, and the consumer can keep using that representation. The opportunity is to turn *data movement and Boolean predicates* into the computation. This card offers design mappings; check exact instruction eligibility, participants and semantics in KernelWiki before implementing them.

## Independent Boolean instances in one word

Represent instance `i` by bit `i` in a word. A bitwise expression then evaluates the same local rule for every represented instance without scalarizing them. For three input planes `a,b,c`, a full-adder stage is:

```text
sum   = a XOR b XOR c
carry = majority(a,b,c)
```

At each bit, `a+b+c = sum + 2*carry`; the carry remains a distinct plane, so no neighboring instance receives it. Compose this with eligibility masks, transition predicates or per-position classifications. A threshold over many inputs can be implemented by a carry-save tree and a final weighted-plane comparison. For exactly three binary inputs and threshold two, `majority(a,b,c)` is already the answer. The representation is exact as Boolean algebra; its GPU cost and its number of live planes are workload questions. (Atlas M01, M06; C00, C37.)

Bit-slicing helps when many independent values undergo the same small rule and the encoded state can survive several transitions. If lanes provide a transposed input, a single ballot-like conversion can make a word-wide circuit possible. Avoid converting back after each stage: for `T` transitions the rough comparison is `encode + T*(plane logic + required neighbor routing) + extract` versus `T*scalar work`. A one-step operation or changing rule per instance may favor scalar/vector code. Cross-word neighborhoods require explicit shifts and carry-in bits; partial warps require a valid-bit mask. Inputs with arbitrary floating state are poor bit-plane candidates unless a justified discretization is part of the caller's contract.

## Let a mask route values

A support mask can carry membership, compact rank and the identity of a next owner. For a participating lane `l`, `rank(l) = popcount(mask & ((1 << l) - 1))` is a simple mapping when the shift is defined for the lane-width boundary. Selection of the `r`th set bit can recover a compact source index; a warp exchange then moves the payload. This can delete an intermediate index array when producer and consumer share the convention. The actual API's sentinel and source-lane rules are part of the design. On SM70, `hw-volta-integer-routing` specifies exact LOP3, PRMT, FNS and warp routing forms; `hw-volta-participation` covers collective membership and ordering, while `hw-volta-feature-boundaries` records generation exclusions.

The same mask can suppress a larger operation when it is empty, encode an ambiguity queue, or represent active graph vertices. A local graph patch may assign vertex `v` to bit `v`; propagation over a fixed neighborhood becomes bitwise intersections/unions, then an explicit boundary exchange handles adjacent patches. This is attractive only if topology is stable and patch state stays local. Dynamic vertex deletion, external identifiers, irregular degrees, or high edge volume can make CSR/bitmap libraries preferable. (Atlas M02, M04, M06, M14; C02, C05, C35.)

For repeated equal keys in a warp, equality groups can share a load, decode or reservation. Reduce once per group, elect an owner and distribute results. An all-distinct distribution is the negative case: matching and leader logic add work with no shared result. Floating-key equality needs the exact equality semantics; a local group is not global deduplication, and reserving a destination is not the same as publishing its payload. Retrieve `hw-volta-participation` for the collective's participant scope and required ordering. (Atlas M05; C04.)

## Small register-resident lookup networks

When a table is tiny and reused, place a few entries in known owners, route to the owning lane, then choose a byte or field from its register. This is a finite routing circuit, not a general register file. A two-level route can represent a slightly larger lookup: select a coarse owner, exchange its word, then select within the word. It may suit a repeated finite-state transition, compact codebook or fixed category map. The cost includes owner selection, exchanges, table updates and every extra payload word. Compare with a direct indexed load, constant-memory broadcast, shared memory and a library/vectorized implementation; uniform and divergent lookups differ. (Atlas M03, M04, M23; C03.)

## Control as data, and the boundary of the trick

Predicates and compact category masks can merge short state transitions and eliminate divergent dispatch. If inactive work is cheap, masked execution may reduce control overhead; if the alternative body is expensive, a real branch or separate path may be better. A short shared rule can be represented as a Boolean function, but one truth table applies uniformly to its input bits; independent per-bit rules require selection or a different representation. A source expression does not prove the expected PTX/SASS lowering.

Strong baselines include packed-byte/vector code, bitset intersection, a normal warp scan, sparse/CSR traversal, and direct lookup. Reject this family if encoding/extraction dominates, required neighbors create a long exchange chain, dynamic indexing spills, or live planes reduce useful residency. A small experiment should first test a scalar reference against exhaustive local truth tables and word-boundary cases, then time equal useful work with full conversions and the best conventional path. The fixed-size graph example should include empty and high-degree patches; the threshold circuit should include all tail masks and values at the threshold.

**Exact fact route:** [KernelWiki contracts](../wiki-contracts.md), especially `hw-volta-integer-routing`, `hw-volta-participation` and `hw-volta-resources`. Keep Atlas E01/E05 as finite semantic/routing evidence and E39's integer carry-chain result scoped to that different operator; neither establishes a general speed ranking. The old Atlas campaign's E11 finding concerns its tested dense 16×16 set-intersection matrix, where packed AND+POPC led; the requested repeated-use sweep actually ran only one iteration. See `hw-volta-atlas-e11-packed-intersection` before treating that result as more than a bounded comparator.

Atlas IDs: M01–M07, M14, M23; C00–C06, C35, C37; E01, E05, E11, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
