# Source locators

Bracketed identifiers in the skill/design are source keys, not maturity labels. Local files were read through Project Control without invoking observer agents. The CUDA skill and Atlas remain separate, continuing sources. Retrieval paths may be mapped to local dependency checkouts by the host; they are not commands to start another agent.

## Local sources

| Key | Workspace / exact path | Role |
|---|---|---|
| KB-README | `kernelbender` / `README.md` | Current component purpose and nonimplementation bootstrap |
| KB-AGENTS | `kernelbender` / `AGENTS.md` | Repository and Todo authority boundaries |
| KB-PLANNING | `kernelbender` / `planning/README.md` | Native workspace root and planning ownership |
| KDA-ENGINE | `kda` / `docs/experiment-engine.md` | Candidate/evaluator interfaces and independent contract boundaries |
| KDA-FLOW | `kda` / `docs/agent-flow.md` | Natural insertion and re-entry points |
| KDA-PROMPT | `kda` / `prompts/basic-flow.md` | Existing docs/draft.md design handoff |
| KDA-CLI | `kda` / `kda_experiments/cli.py` | Registration needs real sources; evidence kinds already defined |
| KDA-STUDY | `kda` / `planning/attention-study-results.md` | Scoped historical study, validated alternatives and baseline race |
| KDA-DIAGNOSIS | `kda` / `runs/attention-decode-study/workspace/docs/profile-diagnosis.md` | Direct decision record and source attribution before merge revision |
| KDA-ATTRIBUTION | `kda` / `runs/attention-decode-study/workspace/evidence/merge-attribution.json` | Combined change and parent-versus-confirmation comparison limits |
| CUDA-ROOT | `skills` / `cuda/SKILL.md` | Current method and operational routing |
| CUDA-MAD | `skills` / `cuda/references/common/machine-aligned-design.md` | Strong existing representation-first method: evaluation baseline |
| CUDA-MECHANICS | `skills` / `cuda/references/common/kernel-mechanics.md` | Fusion, separation, specialization and resource tradeoffs |
| CUDA-VOLTA | `skills` / `cuda/references/architectures/volta/router.md` | Source routing and target-specific scope |
| CUDA-AMPERE | `skills` / `cuda/references/architectures/ampere/router.md` | Ampere source routing; not qualification of every linked guide |
| CUDA-HOPPER | `skills` / `cuda/references/architectures/hopper/router.md` | Hopper routing; exact mechanisms checked in primary docs |
| CUDA-BLACKWELL | `skills` / `cuda/references/architectures/blackwell/router.md` | Blackwell and exact target routing |
| CUDA-HOST | `skills` / `cuda/references/execution/host-execution.md` | Current GPU/controller policy, execution versus read boundaries |
| AT-START | `circuit-bending-atlas` / `START_HERE.md` | Progressive disclosure and evidence/access axes |
| AT-NEED | `circuit-bending-atlas` / `NEED_INDEX.md` | Computational-need to mechanism/composition routes |
| AT-FIELD | `circuit-bending-atlas` / `FIELD_GUIDE.md` | Conceptual design substrate and broader mechanisms |
| AT-R05 | `circuit-bending-atlas` / `reference/R05.md` | Exact native fragment interface versus opaque WMMA |
| AT-R06 | `circuit-bending-atlas` / `reference/R06.md` | Participation, visibility, progress and scope |
| AT-R11 | `circuit-bending-atlas` / `reference/R11.md` | Whole-lifetime economics and useful work |
| AT-R14 | `circuit-bending-atlas` / `reference/R14.md` | Resource interference and execution scope |
| AT-R15 | `circuit-bending-atlas` / `reference/R15.md` | Numerical reinterpretation and finite evidence limits |
| AT-M06 | `circuit-bending-atlas` / `mechanisms/M06.md` | Bit-sliced persistent state |
| AT-M08 | `circuit-bending-atlas` / `mechanisms/M08.md` | Packed integer dots and information loss/range |
| AT-M24 | `circuit-bending-atlas` / `mechanisms/M24.md` | Native bilinear substrate and costs |
| AT-M25 | `circuit-bending-atlas` / `mechanisms/M25.md` | Fragment-native intermediates |
| AT-M37 | `circuit-bending-atlas` / `mechanisms/M37.md` | Restricted copy-engine lead; no public arbitrary API |
| AT-M40 | `circuit-bending-atlas` / `mechanisms/M40.md` | Conditional VMM view construction and nonclaims |
| AT-C00 | `circuit-bending-atlas` / `compositions/C00.md` | Exact Boolean gates; candidate GPU compositions |
| AT-C08 | `circuit-bending-atlas` / `compositions/C08.md` | Integer score representation across consumers |
| AT-C10 | `circuit-bending-atlas` / `compositions/C10.md` | Independent small linear maps with real semantic dimensions |
| AT-C14 | `circuit-bending-atlas` / `compositions/C14.md` | Conditional certified filter construction |
| AT-C16 | `circuit-bending-atlas` / `compositions/C16.md` | Composing producer/consumer ownership |
| AT-C31 | `circuit-bending-atlas` / `compositions/C31.md` | Texture interpolation hypothesis and error contributions |
| AT-C34 | `circuit-bending-atlas` / `compositions/C34.md` | Factored phases instead of mandatory megakernel |
| AT-C35 | `circuit-bending-atlas` / `compositions/C35.md` | Positional identity and metadata removal |
| AT-C36 | `circuit-bending-atlas` / `compositions/C36.md` | Composite layouts across physical granularities |
| AT-C37 | `circuit-bending-atlas` / `compositions/C37.md` | Carry-save per-position thresholds versus aggregate counts |
| AT-C39 | `circuit-bending-atlas` / `compositions/C39.md` | Existing representation-changing search procedure |
| AT-E09 | `circuit-bending-atlas` / `experiments/E09.md` | Tested explicit PTX map versus untested raw WMMA map |
| AT-E39 | `circuit-bending-atlas` / `experiments/E39.md` | Negative/inconclusive full-lifetime bitplane results |
| KW-SKILL | `kernelwiki` / `SKILL.md` | Exact/family retrieval and evidence claims |
| KW-ROUTE | `kernelwiki` / `references/volta.md` | Retained cases and new correctness-only GEMM source boundary |
| KW-LOWBIT | `kernelwiki` / `sources/blogs/volta-grouped-lowbit-measurements.md` | Group skew, decoding placement/engine confounds and measured reuse |
| KW-RECURRENCE | `kernelwiki` / `sources/blogs/volta-recurrence-measurements.md` | State lifetime benefit with combined causal contributions |
| NCU-SKILL | `ncu-report-skill` / `SKILL.md` | Profiler workflow and overlapping activation scope |
| NCU-VOLTA | `ncu-report-skill` / `reference/10-volta.md` | Supported source attribution and missing-metric semantics |
| PC-PLAN | `project-control` / `src/todo_orchestrator/plan.py` | Native v3 validation and persisted task fields |
| PC-GATES | `project-control` / `src/todo_orchestrator/gates.py` | Native gate shape, scope and CUDA admission binding |
| PC-CLI | `project-control` / `tests/test_cli_profiles.py` | Plan validate/apply CLI grammar |
| PC-APPLY | `project-control` / `tests/test_plan_apply.py` | Nonmutating native validation, stale rejection and UUID preservation |

## External primary sources

### STEPBACK — Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models

`https://arxiv.org/abs/2310.06117`

Evidence for an abstraction intervention in studied tasks, not a GPU-kernel efficacy result.
Inspection: Primary abstract/metadata; attempted HTML was unavailable.

### ANALOGY — Large Language Models as Analogical Reasoners

`https://arxiv.org/abs/2310.01714`

Structural/task-relevant analogy as design motivation; examples need grounding.
Inspection: Primary abstract and available article text framing.

### IDEAS — Can LLMs Generate Novel Research Ideas?

`https://arxiv.org/html/2409.04109v1`

Separate novelty, feasibility, diversity and implemented outcomes.
Inspection: Abstract, methods framing and sections 7/10 on diversity, self-evaluation and limitations.

### SELFCORRECT — Large Language Models Cannot Self-Correct Reasoning Yet

`https://arxiv.org/abs/2310.01798`

External checks instead of self-approval as correctness evidence.
Inspection: Primary abstract; scoped to reported models and tasks.

### FUNSEARCH — FunSearch: Making new discoveries in mathematical sciences using Large Language Models

`https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/`

Candidate generation plus external evaluation; no new search engine required here.
Inspection: Author/institution explanation; associated Nature paper identified, full Nature page fetch failed.

### MIRAGE — Mirage: A Multi-Level Superoptimizer for Tensor Programs

`https://arxiv.org/html/2405.05751v3`

Joint algebra, schedule and custom-kernel formulation; formal guarantees do not transfer automatically.
Inspection: Article framing, representation/verification scope; no local reproduction.

### PRISM — Prism: Symbolic Superoptimization of Tensor Programs

`https://arxiv.org/abs/2604.15272`

Symbolic design families versus parameter instantiation.
Inspection: Primary abstract only; HTML fetch unavailable, not an implementation audit.

### FLASH — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

`https://arxiv.org/abs/2205.14135`

IO-aware elimination of conventional intermediates.
Inspection: Primary abstract/algorithm framing, no new reproduction.

### NAPKIN — FlashAttention on a Napkin: A Diagrammatic Approach to Deep Learning IO-Awareness

`https://arxiv.org/html/2412.03317v1`

Composition/resource diagrams as optional reasoning aid, not a required diagram system.
Inspection: HTML article framing and methodology.

### SKILLS-SPEC — Agent Skills Specification

`https://agentskills.io/specification`

Portable SKILL.md metadata and progressive disclosure.
Inspection: Frontmatter, resources, progressive disclosure and validation sections.

### OPENAI-SKILLS — OpenAI: Build skills

`https://learn.chatgpt.com/docs/build-skills`

Explicit/implicit loading and instruction-only skill packaging.
Inspection: Official docs, followed from developers.openai.com/codex/skills; activation and format sections.

### PTX — NVIDIA PTX ISA 8.8, CUDA 12.9.1 archive

`https://docs.nvidia.com/cuda/archive/12.9.1/parallel-thread-execution/index.html`

Exact instruction target/semantics source; not every instruction reaudited.
Inspection: Version identity and relevant documented primitive contracts, complemented by local source study.

### AMPERE — NVIDIA Ampere Tuning Guide, CUDA 12.9.1 archive

`https://docs.nvidia.com/cuda/archive/12.9.1/ampere-tuning-guide/index.html`

Asynchronous staging changes design economics.
Inspection: Relevant architecture tuning sections.

### HOPPER — NVIDIA Hopper Tuning Guide, CUDA 12.3.2 archive

`https://docs.nvidia.com/cuda/archive/12.3.2/hopper-tuning-guide/index.html`

TMA, cluster scope and DPX as generation-specific design contrasts.
Inspection: Relevant primary-source tuning excerpts; no hardware run.

### BLACKWELL — NVIDIA Blackwell Tuning Guide, CUDA 12.9.1 archive

`https://docs.nvidia.com/cuda/archive/12.9.1/blackwell-tuning-guide/index.html`

Exact-generation grounding instead of transplanting an old pipeline.
Inspection: Relevant architecture tuning guide and linked PTX context.

### CUDA-PROGRAMMING — NVIDIA CUDA C++ Programming Guide, CUDA 12.9.1 archive

`https://docs.nvidia.com/cuda/archive/12.9.1/cuda-c-programming-guide/index.html`

Public memory/collective and arithmetic support; native versus emulated intrinsic distinction.
Inspection: Relevant primary documentation excerpts; not a full-document audit.

## Evidence boundaries

A document describing a mechanism is not its qualification on a new binary or target. A source-backed conjecture remains a conjecture; a measured speedup remains scoped to the source, operation, numerical policy and economic boundary. Missing/failed external fetches are recorded rather than silently treated as reviewed full text.

This skill contains new short syntheses and derived examples. Preserve attribution and review licenses before incorporating external code or substantial source text. Private run paths may be locally accessible without being public or portable; absence of the raw artifact limits independent verification.
