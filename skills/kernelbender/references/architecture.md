# Ground a design without freezing it to one GPU

A computational design has two parts: the operator-preserving transformation and the hardware realization. Transfer the former only after checking the latter. A family name, intrinsic declaration or successful build alone does not prove native execution of the desired arithmetic. [PTX, CUDA-ROOT]

## Minimal grounding

For each unusual mechanism establish: exact target and toolchain; operation/operand/output semantics; participant and memory scope; accessible API or permitted instruction form; resource/lifetime constraints; and the status of local evidence. Prefer KernelWiki's architecture-filtered pages and primary source target notes. Query the actual device/toolchain in the implementation environment instead of copying historical ordinals or SKU assumptions.

Use the exact page IDs and query/fetch commands in [KernelWiki contract routing](wiki-contracts.md). In particular, `hw-volta-mma` and its E09 evidence page distinguish a documented explicit PTX coordinate map from the opaque raw layout of WMMA fragments. Keep the exact hardware fact in KernelWiki and the operator mapping in the selected KernelBender construction.

Unknown details can become a small feasibility test. Do not invent register-bank hashes, lane maps, cache coherence, native arithmetic modes or a path to a driver-only engine. Source-level annotation is not proof that state remains in registers. A public primitive can still be a poor economic fit.

## Generational contrasts that change a design

| Target context | Consequence for the design question |
|---|---|
| Volta/V100 SM70 | Explicit half-input MMA/WMMA and ordinary register/shared-memory staging are viable substrates. Native fragment contracts and full-warp participation matter. Keep raw WMMA storage opaque unless independently established. Do not import newer asynchronous copy, warp-group, TMA or TMEM semantics. |
| Ampere, exact supported target | `hw-ampere-async-copy` defines the SM80 cp.async route, eligibility and waits; Tensor Core and shared/L2 changes have separate pages. Revisit the pipeline and error/precision contract rather than transplanting Volta tile choices. |
| Hopper, exact supported target | TMA and cluster/DSM scope can change movement and ownership; DPX can make eligible integer min/max/add recurrences a distinct arithmetic candidate. A cluster is not an arbitrary whole-grid synchronization contract. |
| Blackwell, exact supported target | Different tensor/accumulator mechanisms and target-specific instructions can move the representation boundary again. Consult the actual PTX/KernelWiki contract, including architecture-suffix requirements. Do not treat every Blackwell product or older toolchain as interchangeable. |

These are source-backed orientation contrasts, **not local execution qualifications of KernelBender on all generations**. [AT-R05, AT-R06, AMPERE, HOPPER, BLACKWELL, PTX]

The initial bridge corpus is deepest on Volta because that is where the existing experiments are. Its method should still reason from a different GPU's supported mechanisms. When another target changes the cost or legal scope, adapt the construction and test it; do not clone the entire skill or promise portability of a successful binary. Ampere pointers in the opportunity library identify an architecture route, not an SM70 option.

## Three examples of evidence boundaries

The explicit SM70 `m8n8k4` form examined by Atlas E09 contains four independent small products inside one full-warp collective. This is not permission to execute only an eight-lane subgroup, to reinterpret any WMMA fragment, or to claim that an arbitrary coupled state transition becomes those four independent products. [AT-E09, AT-R05]

Packed four-bit storage can be decoded into a supported compute representation. It does not imply native INT4 or FP4 tensor arithmetic on V100, nor equivalence among two's-complement codes and floating codebooks. [KW-LOWBIT, PTX]

Hopper DPX intrinsics may have software implementations on older devices. A compilable spelling is not evidence of native acceleration, and a packed integer recurrence still needs range/overflow and dependency reasoning. [HOPPER, CUDA-PROGRAMMING]

## Access and source routes

CUDA skill: `skills` workspace, `cuda/SKILL.md`, then the target router and referenced exact guide. Atlas: `circuit-bending-atlas`, `NEED_INDEX.md`, then the relevant mechanism/composition and contract. KernelWiki: its own documented exact-architecture query and page/source following. ncu-report-skill: current `SKILL.md` and generation guide. These are dependency locators, not instructions to launch an observer agent.

Reading a restricted mechanism is allowed research; using driver channels, firmware, binary modification or privileged execution requires separate authorization and validated interfaces. The initial skill normally returns such a path as a research lead alongside an actionable public alternative, not as runnable CUDA code.
