# Sources and confidence boundaries

Use these locators only when their contract or evidence changes the next decision. Local workspace paths refer to the independent sources, not bundled copies. A source can be read directly without invoking an agentic skill/investigator tool. KernelBender carries authored synthesis and original Atlas IDs, not copied Atlas text or artifacts.

## Atlas identity

The Atlas checkout is not redistributed here. Its current source identity is the stable Git revision below; if a checkout is available, inspect a card with `git -C <atlas-checkout> show 5b5629b001da4a42d6f41a84d94f73c07a29d478:mechanisms/M06.md` (substitute the exact card path).

| Key | Workspace / path |
|---|---|
| KDA-ENGINE | `kda` / `docs/experiment-engine.md` |
| KDA-FLOW | `kda` / `docs/agent-flow.md` |
| KDA-PROMPT | `kda` / `prompts/basic-flow.md` |
| KDA-CLI | `kda` / `kda_experiments/cli.py` |
| KDA-STUDY | `kda` / `planning/attention-study-results.md` |
| KDA-DIAGNOSIS | `kda` / `runs/attention-decode-study/workspace/docs/profile-diagnosis.md` |
| KDA-ATTRIBUTION | `kda` / `runs/attention-decode-study/workspace/evidence/merge-attribution.json` |
| CUDA-ROOT | `skills` / `cuda/SKILL.md` |
| CUDA-MAD | `skills` / `cuda/references/common/machine-aligned-design.md` |
| CUDA-MECHANICS | `skills` / `cuda/references/common/kernel-mechanics.md` |
| CUDA-VOLTA | `skills` / `cuda/references/architectures/volta/router.md` |
| CUDA-AMPERE | `skills` / `cuda/references/architectures/ampere/router.md` |
| CUDA-HOPPER | `skills` / `cuda/references/architectures/hopper/router.md` |
| CUDA-BLACKWELL | `skills` / `cuda/references/architectures/blackwell/router.md` |
| CUDA-HOST | `skills` / `cuda/references/execution/host-execution.md` |
| AT-START | `circuit-bending-atlas` / `START_HERE.md` |
| AT-NEED | `circuit-bending-atlas` / `NEED_INDEX.md` |
| AT-FIELD | `circuit-bending-atlas` / `FIELD_GUIDE.md` |
| AT-R05 | `circuit-bending-atlas` / `reference/R05.md` |
| AT-R06 | `circuit-bending-atlas` / `reference/R06.md` |
| AT-R11 | `circuit-bending-atlas` / `reference/R11.md` |
| AT-R14 | `circuit-bending-atlas` / `reference/R14.md` |
| AT-R15 | `circuit-bending-atlas` / `reference/R15.md` |
| AT-M06 | `circuit-bending-atlas` / `mechanisms/M06.md` |
| AT-M08 | `circuit-bending-atlas` / `mechanisms/M08.md` |
| AT-M24 | `circuit-bending-atlas` / `mechanisms/M24.md` |
| AT-M25 | `circuit-bending-atlas` / `mechanisms/M25.md` |
| AT-M37 | `circuit-bending-atlas` / `mechanisms/M37.md` |
| AT-M40 | `circuit-bending-atlas` / `mechanisms/M40.md` |
| AT-C00 | `circuit-bending-atlas` / `compositions/C00.md` |
| AT-C08 | `circuit-bending-atlas` / `compositions/C08.md` |
| AT-C10 | `circuit-bending-atlas` / `compositions/C10.md` |
| AT-C14 | `circuit-bending-atlas` / `compositions/C14.md` |
| AT-C16 | `circuit-bending-atlas` / `compositions/C16.md` |
| AT-C31 | `circuit-bending-atlas` / `compositions/C31.md` |
| AT-C34 | `circuit-bending-atlas` / `compositions/C34.md` |
| AT-C35 | `circuit-bending-atlas` / `compositions/C35.md` |
| AT-C36 | `circuit-bending-atlas` / `compositions/C36.md` |
| AT-C37 | `circuit-bending-atlas` / `compositions/C37.md` |
| AT-C39 | `circuit-bending-atlas` / `compositions/C39.md` |
| AT-E09 | `circuit-bending-atlas` / `experiments/E09.md` |
| AT-E39 | `circuit-bending-atlas` / `experiments/E39.md` |
| ATLAS5B5629B | `circuit-bending-atlas` / checkout `5b5629b001da4a42d6f41a84d94f73c07a29d478`; original Atlas IDs listed beside each synthesis |
| KW-SKILL | `kernelwiki` / `SKILL.md` |
| KW-ROUTE | `kernelwiki` / `references/volta.md` |
| KW-LOWBIT | `kernelwiki` / `sources/blogs/volta-grouped-lowbit-measurements.md` |
| KW-RECURRENCE | `kernelwiki` / `sources/blogs/volta-recurrence-measurements.md` |
| NCU-SKILL | `ncu-report-skill` / `SKILL.md` |
| NCU-VOLTA | `ncu-report-skill` / `reference/10-volta.md` |

## External sources

**STEPBACK — Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models.** `https://arxiv.org/abs/2310.06117`. Evidence for an abstraction intervention in studied tasks, not a GPU-kernel efficacy result. Inspection: Primary abstract/metadata; attempted HTML was unavailable.

**ANALOGY — Large Language Models as Analogical Reasoners.** `https://arxiv.org/abs/2310.01714`. Structural/task-relevant analogy as design motivation; examples need grounding. Inspection: Primary abstract and available article text framing.

**IDEAS — Can LLMs Generate Novel Research Ideas?.** `https://arxiv.org/html/2409.04109v1`. Separate novelty, feasibility, diversity and implemented outcomes. Inspection: Abstract, methods framing and sections 7/10 on diversity, self-evaluation and limitations.

**SELFCORRECT — Large Language Models Cannot Self-Correct Reasoning Yet.** `https://arxiv.org/abs/2310.01798`. External checks instead of self-approval as correctness evidence. Inspection: Primary abstract; scoped to reported models and tasks.

**FUNSEARCH — FunSearch: Making new discoveries in mathematical sciences using Large Language Models.** `https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/`. Candidate generation plus external evaluation; no new search engine required here. Inspection: Author/institution explanation; associated Nature paper identified, full Nature page fetch failed.

**MIRAGE — Mirage: A Multi-Level Superoptimizer for Tensor Programs.** `https://arxiv.org/html/2405.05751v3`. Joint algebra, schedule and custom-kernel formulation; formal guarantees do not transfer automatically. Inspection: Article framing, representation/verification scope; no local reproduction.

**PRISM — Prism: Symbolic Superoptimization of Tensor Programs.** `https://arxiv.org/abs/2604.15272`. Symbolic design families versus parameter instantiation. Inspection: Primary abstract only; HTML fetch unavailable, not an implementation audit.

**FLASH — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness.** `https://arxiv.org/abs/2205.14135`. IO-aware elimination of conventional intermediates. Inspection: Primary abstract/algorithm framing, no new reproduction.

**NAPKIN — FlashAttention on a Napkin: A Diagrammatic Approach to Deep Learning IO-Awareness.** `https://arxiv.org/html/2412.03317v1`. Composition/resource diagrams as optional reasoning aid, not a required diagram system. Inspection: HTML article framing and methodology.

**SKILLS-SPEC — Agent Skills Specification.** `https://agentskills.io/specification`. Portable SKILL.md metadata and progressive disclosure. Inspection: Frontmatter, resources, progressive disclosure and validation sections.

**OPENAI-SKILLS — OpenAI: Build skills.** `https://learn.chatgpt.com/docs/build-skills`. Explicit/implicit loading and instruction-only skill packaging. Inspection: Official docs, followed from developers.openai.com/codex/skills; activation and format sections.

**PTX — NVIDIA PTX ISA 8.8, CUDA 12.9.1 archive.** `https://docs.nvidia.com/cuda/archive/12.9.1/parallel-thread-execution/index.html`. Exact instruction target/semantics source; not every instruction reaudited. Inspection: Version identity and relevant documented primitive contracts, complemented by local source study.

**AMPERE — NVIDIA Ampere Tuning Guide, CUDA 12.9.1 archive.** `https://docs.nvidia.com/cuda/archive/12.9.1/ampere-tuning-guide/index.html`. Asynchronous staging changes design economics. Inspection: Relevant architecture tuning sections.

**HOPPER — NVIDIA Hopper Tuning Guide, CUDA 12.3.2 archive.** `https://docs.nvidia.com/cuda/archive/12.3.2/hopper-tuning-guide/index.html`. TMA, cluster scope and DPX as generation-specific design contrasts. Inspection: Relevant primary-source tuning excerpts; no hardware run.

**BLACKWELL — NVIDIA Blackwell Tuning Guide, CUDA 12.9.1 archive.** `https://docs.nvidia.com/cuda/archive/12.9.1/blackwell-tuning-guide/index.html`. Exact-generation grounding instead of transplanting an old pipeline. Inspection: Relevant architecture tuning guide and linked PTX context.

**CUDA-PROGRAMMING — NVIDIA CUDA C++ Programming Guide, CUDA 12.9.1 archive.** `https://docs.nvidia.com/cuda/archive/12.9.1/cuda-c-programming-guide/index.html`. Public memory/collective and arithmetic support; native versus emulated intrinsic distinction. Inspection: Relevant primary documentation excerpts; not a full-document audit.

## Limits

CUDA and Atlas guidance already contain representation-first reasoning; KernelBender adds a selective construction bridge, not a claim to originate those ideas. External prompting/creativity studies concern their studied models/tasks, not proof of this skill. KDA and KernelWiki measurements are historical examples, not KernelBender evaluations. The KDA merge attribution covers one combined transformation; old unsafe baselines cannot support new speedup claims.

Source/access/qualification are different axes. Correctness samples do not establish all rounding behavior, memory-model legality or performance. Exact target and local execution checks remain necessary. The skill does not replace or automatically update any of these sources.
