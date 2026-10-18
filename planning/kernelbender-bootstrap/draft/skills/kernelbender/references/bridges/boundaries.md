# 10 — Change what crosses an information boundary


**Recognition cue.** Moving, reconstructing or describing data costs more than the useful operation, and the caller permits changing the information exchanged or the view.

**Construction.** Return a compact summary, predicate mask or owner-computed result instead of moving the full payload. Within a device this may be a producer emitting the next consumer's support/format. Across devices it may be a compact request answered by the data owner. A legal virtual-memory view may remove a split-window boundary without duplicating the underlying payload.

Keep the actual API, ownership, lifetime and access contract explicit. A mapped interval does not create uniform locality, coherence or one execution domain. A header describing copy-engine remapping is not a public arbitrary format-transform API. Such material can inspire a public CUDA equivalent or a separately scoped feasibility investigation; it is not executable permission.

**First discriminator.** Compare information volume plus request/setup/service and final materialization, not payload bytes alone. For view changes include mapping granularity, synchronization and translation overhead; compare an optimized ordinary mask/index implementation, not a straw-man modulo loop. For remote ownership include response and scheduling costs.

**Scope boundary.** The initial skill can propose the computation-side opportunity and identify the missing external contract. It does not implement a multi-GPU runtime, manipulate driver channels or start restricted experiments. Preserve a usable public alternative when the exotic path is not currently reachable.

Sources: [AT-M37], [AT-M40], [AT-R14], [CUDA-MAD].
