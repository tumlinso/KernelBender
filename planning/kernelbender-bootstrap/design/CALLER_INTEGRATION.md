# Caller contract and KDA integration

## Inputs: recover, do not require a new manifest

KernelBender accepts ordinary task context and source paths. It does not impose another mandatory JSON contract before the agent can think. Recover these facts from the caller's existing KDA contract, reference implementation and application code:

| Required distinction | What the caller supplies or the agent recovers |
|---|---|
| Observable computation | Equation/state transition, required outputs, visible intermediates and mutation/aliasing behavior |
| Legal specialization | Guaranteed structure/ranges, exact shapes or allowed range, runtime guards and required fallback |
| Numerical semantics | Storage and compute types, intermediate rounding, reordering permission, approximation/error policy |
| Lifetime | Producers, consumers, invariant epochs, update frequency, reuse horizon, invalidation and ownership |
| Economic boundary | Warm kernel/operator/sequence or cold invocation, preparation/transfer costs, capacity and latency constraints |
| Target | Actual architecture/compiler target, toolchain, public API/access limits, caller's source/profiler locators |
| Available evidence | Valid incumbent, prior alternatives, profiles and source/binary identity; explicitly none for a new design |
| Search budget | Scope and allowed implementation effort, available test budget, whether low-level inspection or special access is authorized |

When a fact is missing, read the existing task/source first. State harmless assumptions. Branch on a consequential uncertain value such as reuse rather than inventing it. Return a precise contract question only when no safe design decision can proceed; do not stall every invocation with a questionnaire. Unknown profiling data is not a blocker for a mathematical design hypothesis.

## Outputs: four useful dispositions

Use the same short brief template for `propose`, `probe`, `conventional`, or `blocked-contract`. These are **design recommendations**, not KDA evaluator result/status values.

A useful brief identifies the current implementation convention being challenged; the preserved contract and exploited guarantees; a recommended construction; one serious alternative where helpful; the full-lifetime economic comparison; and the next discriminating test. Include source/evidence locators and unknowns next to the claim they qualify. A single obvious conventional answer can be a paragraph, not a filled form.

The construction must answer where semantic values live, who owns them, how outputs are obtained, what must synchronize, and which operation has actually disappeared. “Use Tensor Cores,” “fuse aggressively,” and “try bitsets” are not constructions. A concise equation, ownership map or pseudocode is appropriate; production CUDA code is not required from the design step.

## Integration points already present in KDA

The inspected `prompts/basic-flow.md` asks the agent to research and write `docs/draft.md` before implementation. Insert an **optional KernelBender design section there**, after the task contract/source inspection and before candidate commitment. In `docs/agent-flow.md`, add a link for structural redesign on later iterations. In `README.md`, document the optional independent skill and its installation path. Do not modify `kda_experiments` or its task JSON. [KDA-FLOW, KDA-PROMPT, KDA-ENGINE]

The bridge is prose plus existing evidence files:

`KernelBender brief → KDA agent implements source → existing register/prepare/evaluate → ncu evidence when useful → updated design brief/next candidate`

Candidate registration requires an actual source directory and manifest. Do not register a design paragraph as if it were a compiled candidate. Translate the brief's hypothesis, change and parent into the existing CLI fields after code exists. No new `design` attachment kind is assumed: KDA currently accepts `profile`, `sass` and `ablation`; keep the design brief in the task's documentation and cite it through ordinary metadata/text. [KDA-CLI]

Experimental variants that change a precision contract belong to separate compatible evaluation groups and require caller permission. A design cannot edit or relax the trusted oracle, workload set or promotion thresholds to make its code win. The KDA agent remains responsible for validating every admitted case and measuring the real objective.

## Re-entry and stopping

Re-enter when the target, output contract, allowed scope, reuse regime or material performance evidence changes, or when local improvements repeat without addressing the same structural limit. Do not re-run all design lenses after a syntax fix. Summarize only what the new evidence changes.

Stop when a feasible direction and its first useful implementation/test are clear, a low-cost probe separates the important alternatives, or the conventional design is already justified. Broad “investigate further” is not a useful return. If a hypothesis loses, preserve which candidate and conditions failed; do not blacklist the entire mechanism family.

## Source and policy precedence

The task/user defines the operation and permitted changes. Primary sources define hardware/API contracts. The CUDA controller governs execution. KernelWiki supplies scoped precedents. ncu-report-skill supplies collected evidence and diagnostics. KDA's task-owned evaluator determines candidate acceptance. KernelBender adds a hypothesis/construction layer only.

Do not resolve apparent policy overlap by editing all existing skills. A greenfield design does not pretend to have profiler evidence; an existing-code bottleneck diagnosis does not pretend hypotheses are measurements. Profiling, explicit-request-only PTX/SASS restrictions and host admission retain their current operational scope. A reference to a privileged Atlas mechanism conveys no permission to run it.

## Repository boundaries

The canonical skill lives in `kernelbender/skills/kernelbender/`. The KernelBender plan owns that component and a task-local KDA consumer fixture. Permanent edits to `kda` are a separate one-task companion plan, applied in the `kda` workspace only after the component is accepted and pinned.

A proposed KDA submodule is `skills/KernelBender`, containing the independent repository. The actual skill entry then lives at `skills/KernelBender/skills/kernelbender/SKILL.md`; documentation/host registration must point to that exact directory. This avoids assuming recursive discovery. The double level is intentional: the component repository also contains research, tests and evaluation records that are not installed as runtime skill context.

An explicit local path to the independent skill also works for the pilot. No service, plugin marketplace, source export daemon, remote model API or automatic installation is required. Inspect the existing host's supported skill registration before adding any optional host-specific metadata. Do not overwrite global skills or install evaluator answer keys.
