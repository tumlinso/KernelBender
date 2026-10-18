# KernelBender

KernelBender is an experimental KDA-compatible design skill for injecting creativity into AI-driven GPU kernel design. Its intended work combines architecture-aware optimization with unconventional experiments and software circuit bending, helping agents explore unusual representations, hardware behavior, composed mechanisms, and novel kernel implementations.

The instruction/reference skill is being implemented from the preserved design package. Its effectiveness is not established. Keep the project lightweight, portable, and compatible with upstream development.

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

Use [`planning/`](planning/README.md) for concise project notes as research and design begin. Task status belongs to the registered Project Control workspace's native Todo authority and should be changed through supported Project Control operations.

## Skill entry

Read [`skills/kernelbender/SKILL.md`](skills/kernelbender/SKILL.md) when a specialized computation has meaningful representation, composition, ownership, or reuse choices. It returns a construction and discriminating experiment to the calling agent; KDA retains implementation, independent validation, and promotion. The skill is portable Markdown and requires no new service. Consumer setup and evaluated status will be recorded with the implementation handoff.
