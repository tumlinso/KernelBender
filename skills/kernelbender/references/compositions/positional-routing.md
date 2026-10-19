# Composition: make position carry identity

**Use when:** the caller repeatedly transports a local object together with a small index or category that is already implied by lane, bit, register slot or fixed local position. A stable position can be an implicit name and a routing coordinate. This can remove metadata loads and address arithmetic, but only while the mapping is shared and stable.

## Construction

Let a warp-local set of active items be represented by a membership mask `m`. For each active lane `l`, its compact rank is the number of active lower lanes. The rank gives a dense output position without storing an input index per item. To materialize payload `v_l`, the consumer selects the corresponding source lane and exchanges its value. Keep the active mask available if the next stage consumes membership. Handle `l == word_width` and empty/no-result sentinels according to the actual API rather than a hand-written shift that may be undefined. (Atlas M02, M04; C04, C35.)

The same positional identity can represent a small routing network. Store a fixed finite table in known lane/register owners. First route a key to a table-owning lane, then select within its held entries; for a bounded payload, compose coarse lane selection with within-word byte/field selection. For a graph tile, assign a stable local vertex index to a bit or lane. Neighbor identity can become a shift, bit mask or lane route instead of an explicit gather-index array. Restore external IDs only at the boundary that truly requires them. (Atlas M03, M04, M14, M23; C03, C05, C35.)

Equal keys may be grouped by a warp match operation. Elect one leader per group to load a shared parameter, compute once or make a single output reservation; then distribute the group result. This is a local grouping circuit. All-distinct inputs are the control case because leader-election overhead may have no reuse to amortize. A reservation and a publication are separate events; the consumer needs the proper ordering contract before seeing payload. (Atlas M05; C04.)

## A concrete local graph recipe

For a warp patch with at most one vertex per lane, keep `active` and `visited` as masks. If each vertex's local successor set fits a word, let `succ(v)` be an owner-local mask. A lane owning `v` can contribute `succ(v)` when its active bit is set; a warp-level reduction of these masks forms the next frontier. Then suppress already visited vertices and continue with `next = union_succ & ~visited`. For larger neighborhoods, route the successor words by a compact owner map or stage them in a suitable memory representation. The result is a construction to test when the consumer needs only a compact local frontier, not arbitrary edge payloads. Check that the set union is the correct graph operator and that duplicate destinations are harmless under its Boolean algebra.

The conventional control is an adjacency-list/CSR traversal or a library graph primitive on the same patch/degree distribution. The positional method loses if the patch is sparse but pays for many padded lanes, if adjacency does not fit the selected word/routing scope, or if global ID restoration and synchronization dominate.

## Contracts and economic boundary

Explicitly list the reversible map from local position to external identity and the point where that map changes. Reordering, deletion, compaction or dynamic topology may invalidate it. Do not use an SM ID, transient block order or a physical scheduling observation as semantic identity. Rank/select only yields an ordinal; it does not fetch arbitrary payload by itself. Shuffles only move values among valid participants, and multiword values need multiple operations. For SM70, `hw-volta-integer-routing` owns the exact LOP3/PRMT/FNS and ballot/shuffle/match forms; `hw-volta-participation` owns the wider ordering, visibility and progress rules.

Count initial classification, ballot/match, rank/select, routing, reservations, payload movement and ID recovery over the full pipeline. A small map rebuilt once and used many times can be worthwhile; rebuilt every stage it may not be. Test a labeled one-hot mapping first, then tail and empty cases, then equal and all-distinct keys, and only then measure against the strong packed or graph baseline. Use `hw-volta-participation`, `hw-volta-resources` and `hw-volta-feature-boundaries` for target scope; exact map/selector behavior comes from the corresponding Wiki source.

**Failure signal:** the receiver does not share the positional convention, the needed lane is inactive, the selected owner does not hold the requested payload, or index reconstruction costs as much as the metadata removed. In those cases retain explicit indices or choose a supported library.

Atlas IDs: M02–M05, M14, M23; C03–C05, C35, C36; E05, E14. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
