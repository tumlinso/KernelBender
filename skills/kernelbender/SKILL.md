---
name: kernelbender
description: Design specialized, fused, or repeatedly reused GPU computations by reconsidering their representation, ownership, algorithm and kernel boundaries. Use for new custom operators, structural performance limits, or explicit requests for unconventional designs. Not a replacement for routine CUDA help, profiling or KDA evaluation.
---

# KernelBender

Help the caller invent a useful computation, not merely a more unusual implementation. Start from what must be observed and what may legitimately change. Supply concrete architectural substrate and a testable construction; novelty alone is not success.

You are the calling agent using a design skill. This design step does not launch a hidden agent, optimizer or background process. Keep any caller-authorized delegation in the existing KDA workflow. The current task contract and execution permissions remain authoritative.

## Decide whether a design intervention is useful

Use this skill before committing a specialized operator to conventional layouts, when composition/reuse may remove work, or when evidence suggests the current representation is the limiting factor. A strong conventional/library solution is a valid outcome. An explicit request to rethink a problem deserves that consideration; do not dismiss it simply because a library exists.

For an ordinary API question, routine tuning or a known correctness repair, use the corresponding CUDA/KernelWiki/profiling route instead of forcing a creativity exercise. For an existing hotspot, read the available profile and source. For a new computation, there need not be a profile: distinguish predicted cost and hypotheses from measured bottlenecks.

## Reframe around the caller

Recover the equation/state transition, observable outputs, permitted numerical behavior, true input guarantees, target and full cost boundary from the existing task. Follow values backward from the consumer and forward through updates and reuse. Separate required semantics from conventions inherited from a reference implementation.

What must be materialized? What is fixed for an epoch rather than every call? Which relationships could be represented by a bit, position, lane, register slot, native fragment, sparse support or a mergeable summary? What would invalidate that representation? Do not assume that a repeated benchmark input is an immutable application input.

Use [caller and lifetime questions](references/caller.md) for missing details. Read supplied context before asking. Preserve consequential unknowns as conditional branches or a precise missing-contract question, not invented facts.

## Connect a few relevant mechanisms

Use the [need map](references/need-map.md). When the ten bridges do not provide enough technical substrate, use the [problem-first opportunity index](references/opportunity-index.md) to open one relevant affordance and, if useful, one construction. Do not load every card or fill a quota of ideas. The library is a source of candidates, not a mandate to use exotic hardware.

| Open design choice | Bridge |
|---|---|
| Full intermediate or only the demanded result? | [Demanded information](references/bridges/demand.md) |
| Recompute, prepare once, or maintain across uses? | [Lifetime and reuse](references/bridges/lifetime.md) |
| Canonicalize each stage or compose their layouts? | [Ownership maps](references/bridges/ownership.md) |
| Scalar categories/counts or parallel Boolean state? | [Bitplanes and thresholds](references/bridges/bitplanes.md) |
| Explicit metadata or stable positional structure? | [Identity and routing](references/bridges/identity.md) |
| Familiar arithmetic or another native computational resource? | [Arithmetic domains](references/bridges/arithmetic.md) |
| Sequential work or a mergeable sufficient summary? | [Dependency factoring](references/bridges/summaries.md) |
| One big fused unit or a different work/phase distribution? | [Parallelism and phase boundaries](references/bridges/parallelism.md) |
| Expensive exact work everywhere or a justified fast filter? | [Approximate then refine](references/bridges/refinement.md) |
| Move full payloads or change a permitted information boundary? | [Boundaries and views](references/bridges/boundaries.md) |

Use [architecture grounding](references/architecture.md) to check exact target, primitive, participation and access. A cross-domain or cross-generation analogy must explain the operator-preserving correspondence and what does **not** transfer. You may propose unlisted mechanisms when useful; source or test their contract instead of inventing hardware behavior. Restricted Atlas ideas remain research leads unless separately authorized.

The [KernelWiki contract map](references/wiki-contracts.md) gives exact page IDs for architecture and evidence retrieval. KernelBender cards hold the computational construction; KernelWiki owns exact instruction, layout, numerical, memory and synchronization facts.

## Construct a small set of genuinely different designs

Keep the strongest applicable conventional route. When warranted, construct one or two alternatives that change representation, lifetime, algebra, ownership, work partition or an information boundary—not merely tile sizes. No minimum count is required.

For each serious option, show the semantic equation, representation through its lifetime, producer/consumer ownership and how outputs are obtained. Identify the guaranteed property it exploits. Count added packing, extraction, invalidation, maintenance, synchronization and live-state costs alongside removed work. Compare the complete permitted region, including setup when the caller pays it.

For reuse, check whether recurring saving actually exceeds preparation and updates; more uses do not rescue a recurring path that is slower. Register state does not survive ordinary kernel completion. Fewer bytes, higher occupancy and a novel instruction are not independently the objective.

Separate invention from acceptance. Reject a violated contract or unsupported instruction; do not reject a plausible new family solely because a coarse estimate is uncertain or one dated implementation lost. Preserve an inexpensive discriminating option when it could change the choice.

## Return a decision and the next informative action

Use a compact [design brief](assets/design-brief.md), or a short paragraph for a simple conventional decision. Return `propose`, `probe`, `conventional`, or `blocked-contract` as prose—not as a KDA engine status.

Identify the chosen construction, its serious alternative, source-backed rationale, semantic/numerical obligations and the first test that could reject it. Distinguish feasibility, causal attribution and full-path advantage. Use [experiment guidance](references/experiments.md). Do not claim that speculative novelty, a passing small test or profiler replay time establishes a speedup.

Write the brief into the current task's `docs/draft.md` when using KDA. The KDA agent then implements a candidate and uses the existing independent validator and experiment engine. Do not mutate trusted references, numerical thresholds or workload definitions to make a candidate win. Do not register an unimplemented idea as source code.

Re-enter only when evidence or the caller's constraints materially change. Preserve failed shapes and useful counterexamples; propose reviewed knowledge updates rather than silently changing KernelWiki or the Atlas. The objective is a better engineering choice, not endless exploration.

## Concrete examples and sources

[Consumer-specific projection](examples/consumer-projection.md), [per-position mask thresholds](examples/mask-threshold.md), [attention merge diagnosis](examples/attention-merge.md), [decoding versus preparation](examples/lowbit-lifetime.md), and the [dense-library control](examples/dense-library-control.md) illustrate different uses and failure boundaries. They are examples, not an exhaustive design vocabulary.

[Source locators and evidence boundaries](references/sources.md) identify the continuing CUDA skill, Atlas, KernelWiki, ncu-report-skill, KDA study and external primary references. These sources inform the design; they do not override task or host policy.
