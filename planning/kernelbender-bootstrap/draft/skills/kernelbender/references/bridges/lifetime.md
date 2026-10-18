# 02 — Choose representations across preparation, updates and reuse


**Recognition cue.** The same topology, coefficient table, packed weight or state encoding is used repeatedly. Per-call optimization may hide the decisive preparation/invalidation boundary.

**Construction.** Separate what is fixed at code generation, parameter update, batch and individual use. A static categorical rule can be compiled into a Boolean circuit; a changing state may remain encoded across many rule applications. A packed weight can be fully decoded once, decoded into native consumer tiles, or decoded repeatedly near each use. These are different storage and lifetime contracts, not just different load instructions.

For n uses and u updates, compare `P + n*C + u*M + E`, including preparation P, per-use cost C, maintenance M and extraction E. If all terms vary with shape, compare regimes rather than invent one crossover number. When a measured recurring path is slower, more reuse does not make it faster unless another shared cost actually changes.

**Failure boundaries.** State in registers lives only within a real execution lifetime. Concurrent users, parameter mutations, aliasing and eviction need correct ownership/invalidation. A compressed representation can save capacity while losing throughput; report both honestly.

**First discriminator.** Hold the represented input/operation fixed and compare cold epoch cost, repeated resident use and a real update. Track bytes/calls actually paid; do not credit harness fixture/oracle I/O as production setup. Keep the best materialized baseline.

**Counterexample already known.** KernelWiki's direct W4A16 SIMT decoder lost to predecode+cuBLAS in its tested cases. It changes both decode placement and arithmetic engine. That limits the implementation, not the whole family of consumer-native decoding designs. Sources: [AT-R11], [AT-E39], [KW-LOWBIT], [KW-RECURRENCE].
