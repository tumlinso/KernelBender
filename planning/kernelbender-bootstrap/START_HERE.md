# KernelBender — design and Todo bootstrap

**Prepared:** 18 October 2026. **Destination workspace:** `kernelbender`.

KernelBender should help a kernel-design agent discover **what computation and representation to build for the caller's particular problem**, rather than merely tune a familiar implementation. Its distinctive contribution is a usable connection from application structure to unfamiliar computational mechanisms, with the representation's whole lifetime and a concrete next experiment attached.

This delivery is research, design, drafted skill material and implementation tasks. It is **not** a claim that the skill has been installed, that the Todo plans have been applied, or that KernelBender has demonstrated a performance benefit. No agentic Project Control tools were invoked, no GPU work was run, and no user repository was modified.

## Read these first

1. [DESIGN.md](DESIGN.md): the decision, why this is different from the existing CUDA guide, and alternatives rejected.
2. [Implementation work](planning/WORK.md) and [intake](planning/INTAKE.md): seven component tasks plus a closing aggregate; one separate, narrowly scoped KDA integration plan.
3. [Draft skill](draft/skills/kernelbender/SKILL.md): preassembled runtime instructions, ten mechanism bridges and worked examples. Adopt and refine these; do not repeat the entire research phase.
4. [Evaluation](design/EVALUATION.md): test against the *current competent stack*, including its machine-aligned CUDA guidance and Atlas access, not a deliberately weak baseline.

## Main decisions

- A selectively invoked, instruction-and-reference skill. No new model, agent controller, compiler, profiler, vector database, or population-search engine.
- The same calling agent remains responsible for design and implementation. The skill changes the questions and context it uses; it does not run a hidden second agent.
- Design the smallest **complete economic region**: a kernel, composed operator, or retained representation across calls, depending on what the caller permits. Do not equate the unit of optimization with one launch.
- Use a flexible sequence: recover the real contract; expose representation choices; connect relevant mechanisms; compare unlike designs; return one recommended construction or discriminating probe. It is not a quota for strange ideas.
- Initial material is broad in computational concepts, deepest on Volta, with documented Ampere/Hopper/Blackwell contrasts. Hardware execution qualification is recorded separately from conceptual coverage.
- Keep CUDA execution controls, KernelWiki, ncu-report-skill and KDA evaluation authoritative in their domains. The CUDA skill and Atlas continue unchanged; this is one better replacement *candidate*, not their retirement.

## Deliverables in this directory

| Location | Purpose |
|---|---|
| `design/` | Research synthesis, caller/integration contract, knowledge design and fair effectiveness evaluation |
| `draft/skills/kernelbender/` | Proposed portable skill and material, not automatically installed |
| `evaluation/` | Six reviewer scenarios and a bounded native pilot specification; no invented results |
| `integration/` | Exact KDA insertion points and a proposed small workflow addition |
| `sources/` | Local source identities, external references, limitations and corrections |
| `planning/` | Native Todo v3 files, meaningful task notes and safe application procedure |
| `scripts/check_package.py` | Offline structural check of this delivery only |
| `validation/` | Actual checks and explicit checks not run |

Copy the complete package into `planning/kernelbender-bootstrap/` in the standalone KernelBender repository before native plan intake. Preserve its relative layout. The canonical skill destination proposed by this package is `skills/kernelbender/`, separate from research and private evaluation material. Do not install the bootstrap's evaluation answer notes as part of the skill.

**Implementation uses the already integrated KDA engine and the Volta port at `~/ncu-report-skill`.** Their current interfaces and source identities still need to be checked at consumption time. Availability of newer GPUs broadens the design substrate; it does not justify assuming that a documented feature or an old result applies to an unqualified target.
