# Atlas consolidation coverage

This inventory records ownership decisions for the current staged migration. It
does not certify that the Atlas or CUDA skill has been replaced. Both remain
authoritative source material until a separate completeness and qualification
review.

## Active ownership

KernelBender receives authored computational constructions and design-search
guidance. Its entry stays selective: the ten bridges route to the problem-first
opportunity index, which points to a small number of affordance and composition
cards. The current authored destinations include:

- Bit and routing circuits: skills/kernelbender/references/affordances/bit-routing.md.
- Arithmetic and tensor resources: affordances/arithmetic-tensor.md.
- Operand flow and retained ownership: affordances/operand-flow.md.
- Cross-actor/system boundaries: affordances/system-boundaries.md.
- Discrete state, arithmetic, tensor, positional-routing, screening, ownership,
  phase, and communication compositions under references/compositions/.
- Need-first routing: references/opportunity-index.md; exact facts are routed
  through references/wiki-contracts.md.

These files explain what to construct and how to falsify it. They retain
conventional/library baselines, complete-path costs, mathematical assumptions,
and uncertainty. They do not turn an Atlas hypothesis into a performance
recommendation.

KernelWiki receives the exact target contracts and selected bounded empirical
records. The current Volta lane enriches existing hw-volta-mma,
hw-volta-resources, hw-volta-participation, hw-volta-feature-boundaries,
hw-volta-numerics, and hw-volta-operand-delivery. The new machine-contract
page hw-volta-vmm-addressing owns public VMM details. The separate
hw-volta-atlas-e09-mma-coordinate page records a bounded coordinate check; it
is an evidence summary, while the exact instruction contract remains in
hw-volta-mma. Experimental summaries have separate pages for E09, E11, E12,
E16, E23, and E39, with E10 connected to the numerical page. The evidence
index hw-volta-atlas-evidence-index records all forty campaign dispositions.
KernelWiki's Ampere route now has separate pages for async copy, tensor
operations, and memory resources; those pages are SM80 contracts and are not
Volta extensions.

The detailed ID-level split is in CROSSWALK.md. Original IDs remain visible in
KernelBender provenance markers and KernelWiki evidence/source metadata.

## Retained and incomplete material

The Atlas source remains intact at its original revision. It remains the
authoritative full record for design hypotheses, complete experiment
protocols, campaign portable summaries, authoring history, and source
capsules. The active migrations intentionally do not copy the Atlas
compendium, raw artifacts, benchmarks, navigation reader, or the 148-card
corpus wholesale.

KernelWiki's current migration prioritizes reusable facts needed by the selected
KernelBender constructions. The new hw-volta-integer-routing page owns exact
Volta LOP3, __fns, PRMT, warp match/shuffle, and DP4A contracts. Packed SIMD
conversion and saturation details remain routed to CUDA's versioned SIMD
intrinsic documentation until the Wiki page covers them. In all cases
hw-volta-feature-boundaries records generation exclusions, not the detailed
primitive contract. A dedicated architecture page is also still warranted
before treating all Atlas
claims about NVLink pair topology, host NUMA ingress,
peer atomics, texture/SFU pathways, fault/access-counter policy, every
copy-engine interface, counters, MPS, RAS, and power behavior as a complete
KernelWiki reference. Until then, use exact existing Wiki pages and their
source records where applicable, and retain Atlas-only factual detail at the
pinned source revision. Do not invent an authority page by extending a broad
Volta page with unrelated claims.

E00–E08, E13–E15, E17–E22, E24–E26, E31–E38 remain discoverable in the
KernelWiki evidence index but do not receive a dedicated detailed page in this
stage. Their result scope, status, and limitation stay attached to the original
Atlas experiment/evidence locator. This is deliberate: the status index is a
route, not a restatement of every campaign protocol.

The five NOT_RUN campaign items are not converted into negative findings:

- E04 (register-bank/reuse question) and E27–E30 (restricted remap, command
  actor, QMD dependency, and binary edit) remain unmeasured.
- Other GPU_RUN cards describe bounded implemented subsets, not necessarily
  completion of the original protocol.
- E21's node-1 binding failed; its completed node-0 cases are not a NUMA
  comparison.
- E17 used unequal data movement, so it does not establish equal-work overlap.
- E26 provides finite approximation observations rather than a worst-case
  bound.

No GPU experiment was required or run for this migration. The Atlas's portable
checks were run offline; see PROVENANCE.md. KernelBender and KernelWiki do not
gain a profiler, optimizer, scheduler, experiment runner, candidate registry,
or execution service. KDA remains responsible for correctness gating,
benchmarking, evidence retention, and promotion.

## Replacement boundary

The repositories have different responsibilities and neither is a complete
replacement for the source corpora yet:

- KernelBender is a selective library of design transformations and concrete
  candidate constructions. It cannot establish machine legality or measured
  performance.
- KernelWiki is an architecture-filtered machine/evidence reference. It is not
  a generative design guide and does not contain every Atlas hypothesis.
- The CUDA skill remains the broader practical programming and engineering
  reference across Volta, Ampere, Hopper, and Blackwell.
- The Atlas remains a useful historical and research archive, especially for
  unmeasured and restricted-interface questions.

Full CUDA-skill retirement still needs a separate architecture and workflow
coverage audit, notably for practical engineering procedures and complete
Ampere/Hopper/Blackwell equivalence. No removal or supersession claim is made.
