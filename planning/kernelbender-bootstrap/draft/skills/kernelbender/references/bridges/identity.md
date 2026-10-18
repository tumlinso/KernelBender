# 05 — Turn stable position into metadata and routing


**Recognition cue.** A small graph, neighborhood, category block or stencil repeatedly loads IDs whose relationships are stable and local.

**Construction.** Assign local objects to bits, lanes or slots so position carries identity. For up to 32 local vertices, a neighbor support mask can replace a loop over integer neighbor IDs for membership/intersection queries. A warp vote can form a mask; rank/select can compact only where the caller actually needs external IDs. A shuffle network can route values among participating lanes when the required value is in the declared source slot.

The map must be explicit and reversible at observable boundaries. A Boolean membership query and weighted graph accumulation are different operators: the mask alone does not preserve weights or multiplicity. Dynamic edges, deletions and reordering can make mapping maintenance dominate.

**First discriminator.** Compare the whole patch operation with a strong CSR/packed-support baseline. Include external-to-local mapping, cross-patch edges, output ID recovery and the actual update frequency. Check duplicate edges/updates according to the specified algebra. One-lane-per-object is a candidate, not a theorem that every patch fits a warp efficiently.

**Failure boundary.** A physical SM ID or transient scheduling identity is not a stable application name. A shuffle needs participating sources and defined values; multiword movement costs multiple operations. Remove metadata only when both ends genuinely share the convention.

Sources: [AT-C35], [AT-NEED], [AT-R06], [CUDA-MAD].
