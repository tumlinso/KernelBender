# KernelBender

KernelBender is an experimental KDA-compatible design skill for injecting creativity into AI-driven GPU kernel design. Its intended work combines architecture-aware optimization with unconventional experiments and software circuit bending, helping agents explore unusual representations, hardware behavior, composed mechanisms, and novel kernel implementations.

The portable instruction/reference skill is implemented and remains optional and experimental. In the bounded native pilot, all nine baseline/candidate binaries across three task families passed qualification. The Boolean transition B kernel was promoted at 2.890× its task baseline; the task baselines were retained for observable energy and dense GEMM. Matched probes did not establish incremental skill benefit, and no causal skill-level win is claimed. The original pilot validation included 22 CPU tests and 10 driver tests. See the [evaluation report](evaluation/REPORT.md) and [implementation handoff](planning/IMPLEMENTATION-HANDOFF.md) for evidence and limits.

The Atlas consolidation adds a [problem-first opportunity library](skills/kernelbender/references/opportunity-index.md), four affordance families, eight composition families, and an [exact KernelWiki contract map](skills/kernelbender/references/wiki-contracts.md), behind the existing ten bridges. Its [migration crosswalk](planning/atlas-consolidation/CROSSWALK.md), [coverage report](planning/atlas-consolidation/COVERAGE.md), [provenance](planning/atlas-consolidation/PROVENANCE.md), and [validation report](planning/atlas-consolidation/VALIDATION.md) distinguish authored constructions, machine contracts, bounded observations, and remaining gaps. The original Atlas and CUDA skill remain intact and authoritative source material. New [design fixtures](evaluation/atlas-consolidation/blind-fixtures.md) and CPU/retrieval checks qualify the expanded content; they do not extend the earlier native pilot's performance or skill-effectiveness claims.

## Relationship to related work

KernelBender is intended to complement:

- **KDA (Kernel Design Agents):** the broader agent-centered workflow for researching, implementing, verifying, and iterating on performance-sensitive GPU kernels. KernelBender may contribute a creativity-oriented method within that workflow.
- **KernelWiki:** architecture and kernel knowledge that can inform candidate designs and optimization choices.
- **ncu-report-skill:** profiling reports and performance evidence that can help explain and assess candidate kernels.
- **Circuit-Bending Atlas:** a collection of mechanisms, representation ideas, composition hypotheses, and experimental evidence that can inspire unconventional computation.

These are related projects and sources of context. The skill uses their scoped evidence and existing workflows without bundling their implementations or replacing their authority.

## Development and evidence

Keep changes small and easy to review. Preserve portability and upstream compatibility, and record assumptions that affect behavior. For kernel work, establish correctness before comparing speed. Distinguish ideas and hypotheses from source-backed rationale and measured results; make measurements reproducible by recording the relevant hardware, software, workload, and method. Follow [AGENTS.md](AGENTS.md) for repository conventions.

## Planning

Use [`planning/`](planning/README.md) for concise project notes as research and design continue. Task status belongs to the registered Project Control workspace's native Todo authority and should be changed through supported Project Control operations.

## Skill entry

Read [`skills/kernelbender/SKILL.md`](skills/kernelbender/SKILL.md) when a specialized computation has meaningful representation, composition, ownership, or reuse choices. It returns a construction and discriminating experiment to the calling agent; KDA retains implementation, independent validation, and promotion. The skill is portable Markdown and requires no new service. The evaluation report and implementation handoff record the current consumer boundary, evidence, and limits.
