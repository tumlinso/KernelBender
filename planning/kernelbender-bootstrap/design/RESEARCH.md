# Research synthesis and limits

This is decision support, not a literature survey for its own sake. The references were chosen to test whether a small skill intervention is defensible and what material it should contain. Exact source URLs, local hashes and inspection scopes are in `sources/`.

## What the local sources already solve

**CUDA / machine-aligned design** already provides semantic framing, unlike candidates, ownership, complete costs and falsifiers. KernelBender must outperform that baseline, not claim to invent it. Its likely added value is better problem-driven access to computational mechanisms and more concrete construction of specialized compositions. [CUDA-ROOT, CUDA-MAD]

**Atlas** provides native primitives, composition hypotheses, formal boundaries and dated measurements. C39 is a useful prior method, but its recommended three candidate classes are not empirical proof that a mandatory three-way ritual is best. E39's near-tie for one bitplane cell has an uncertainty interval crossing zero; it is not a reusable win. E09 verifies the explicit tested PTX mapping, not raw WMMA ownership. [AT-C39, AT-E39, AT-E09]

**KernelWiki** provides useful retained baselines and scope-qualified results. The low-bit experiment changes both where decoding happens and the arithmetic engine; it cannot isolate the cost of decoding location. The recurrence comparison combines launch count, lifetime and state ownership; it does not isolate HBM traffic. These are ideal teaching cases about useful observations versus causal explanation. [KW-LOWBIT, KW-RECURRENCE]

**KDA** already has the evaluator needed for consequential experiments. Its attention study kept the parent's partial kernel unchanged and replaced the merge as one combined transformation. The direct attribution record supports that combined change, not separate causal claims about every instruction. The baseline race and failed mixed candidate show why sampled numerical correctness alone is not enough. [KDA-ENGINE, KDA-STUDY, KDA-DIAGNOSIS, KDA-ATTRIBUTION]

**ncu-report-skill** supplies supported counters, source attribution and diagnosis. Its broad “profile before planning” slogan is not a prerequisite for an unimplemented computation. The integration must distinguish speculative design from measured diagnosis without changing the profiler's own scope. [NCU-SKILL, NCU-VOLTA]

## Relevant external findings

| Source | What it supports | Design consequence | What it does not establish |
|---|---|---|---|
| Step-Back Prompting [STEPBACK] | Abstraction cues improved selected reasoning tasks in the studied models | Begin with the required computation rather than low-level inherited details | That this prompt improves GPU kernel design or the present model |
| Analogical Reasoners [ANALOGY] | Task-relevant analogies/exemplars improved studied reasoning and code tasks | Retrieve by structural correspondence; explain what transfers and what breaks | Generated examples are true hardware evidence |
| Expert research-idea study [IDEAS] | Novelty judgments, feasibility concerns, duplication and unreliable self-ranking are distinct | Do not select solely by the model's novelty/confidence; evaluate implemented outcomes | A universal deficit of all present/future models or proof of KernelBender benefit |
| Intrinsic self-correction study [SELFCORRECT] | Self-revision without external feedback can fail in studied reasoning settings | Use semantic checks, trusted references and experiments, not repeated self-approval | That critique is never useful, or that those results measure kernel design |
| FunSearch [FUNSEARCH] | Candidate programs plus an external evaluator can support discovery | Let KDA test constructions and preserve informative alternatives | A need to add an evolutionary engine or a guarantee of unrestricted discovery |
| Mirage [MIRAGE] | Joint algebraic and execution-level transformations enable optimization beyond fixed schedules | Keep formulation, ownership and fusion decisions coupled | Its formal search/verification guarantees transfer to free-form LLM design or arbitrary floating arithmetic |
| Prism [PRISM] | Abstract describes symbolic design families before parameter instantiation | Distinguish structural design families from tile-parameter variants | An audited algorithm result here; only the abstract was inspected |
| FlashAttention [FLASH] | IO-aware reformulation can eliminate materialized intermediates | Ask which information the consumer needs, not only which operator to speed up | Every fused design wins, or every numerical ordering is interchangeable |
| FlashAttention on a Napkin [NAPKIN] | A compositional representation connects algorithms to resource/distribution models | Use compact lifetime/ownership sketches and explanatory cost models | A requirement to implement diagram tooling or a validated performance simulator |
| Agent Skills specification / official host docs [SKILLS-SPEC, OPENAI-SKILLS] | On-demand instruction/reference loading and a portable entrypoint | Start instruction-only, short metadata, focused references, explicit invocation fallback | Guaranteed activation, tool authorization, or hard context isolation |

The material proposed here is our engineering synthesis. No cited paper evaluates this exact skill against the user's KDA stack. Preserve that uncertainty and test the actual intervention.

## Three conclusions from comparison, not imitation

**Structural analogy is more useful than topical similarity.** A warp network can resemble local graph routing; bitplanes can resemble a vector of Boolean machines; online reduction state can resemble a mergeable summary. The important relation is an operator-preserving mapping. A story that two domains both use “attention” or “circuits” is insufficient.

**Nonlocal design can need a locally worse step.** Packing or a wider intermediate may cost more at one boundary but remove repeated future work. Compare the permitted lifetime, not a greedy per-operator score. Conversely, reuse is not a magic multiplier when the recurring path itself is slower.

**The final judge must be the right observable.** Speculative candidates can be ranked by a reasoned cost model for the next experiment. Promotion requires the true operator, numerical policy and economic scope. Human/LLM ratings of cleverness are secondary diagnostics, not the target.

## Current-source caution

Online software documentation changes; record the fetched version and exact target. Newer compiler support and hardware features are not assumed from an architecture-family label. The package supplies illustrative generation contrasts but delegates exact instruction form, numerical mode and installation qualification to the corresponding primary source, KernelWiki and actual toolchain. Existing CUDA/Atlas operational policy is not displaced by a skill recommendation.
