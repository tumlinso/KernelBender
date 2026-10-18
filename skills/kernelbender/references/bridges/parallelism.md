# 08 — Redistribute useful work and deliberately choose phase boundaries


**Recognition cue.** Too few independent tiles, a serialized consumer, heavy tails, or a fused region with an excessive instruction/live-state working set.

**Construction.** Split an independent dimension into partials and a valid merge; group work sharing a producer without mixing distinct outputs; or factor a large computation into a small hot phase plus infrequent/awkward paths. Optimize the partial layout and merge together. More CTAs can repay partial-state traffic in one regime and lose badly in another.

The KDA attention study is an instructive example: the parent's partial kernel stayed unchanged while a combined parallel-weight and feature-ownership merge revision was tested. The design targeted a dependent merge rather than assuming that low DRAM throughput meant bandwidth saturation. Its evidence attributes the combined redesign, not every individual instruction change. [KDA-DIAGNOSIS, KDA-ATTRIBUTION]

**First discriminator.** Change a meaningful partition/owner boundary while holding the operator and numerical contract fixed. Include all partials, merge launches and work distribution. Measure ordinary full-operator timing; use profiles to investigate the responsible bottleneck. A few same-family parameter choices help find a crossover, but do not masquerade as design diversity.

**Failure boundary.** Persistent work requires a bounded schedule and progress argument. It is not automatically better than batching/graphs. A consumer that reserves the resources its producer needs can deadlock. Conversely, reducing live state by materializing a boundary can beat an all-register megakernel.

Sources: [AT-C34], [AT-R06], [AT-R14], [CUDA-MECHANICS], [KW-RECURRENCE].
