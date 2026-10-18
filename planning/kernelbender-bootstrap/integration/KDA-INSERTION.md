# Small KDA integration change

This is a proposed change for the separately scoped KDA task, not a patch already applied.

## `prompts/basic-flow.md`

After workspace/contract inspection and before committing the implementation draft, add:

> When a task has meaningful specialization, composition, representation or reuse freedom—or the caller explicitly requests a structural rethink—consult KernelBender before fixing the algorithm and kernel boundaries. Put its concise design decision and first discriminating experiment in the existing `docs/draft.md`. A conventional/library route remains valid. No profile is required for a new design; use existing profiling evidence for a measured hotspot. Keep the task's independent numerical/semantic contract and the normal KDA evaluation loop authoritative.

Do not call it automatically after every compile, force a fixed number of candidates, or add another required task-manifest field.

## `docs/agent-flow.md`

Link the installed skill and describe later re-entry when evidence exposes a structural limit or the caller's reuse/output/target constraints change. Once representation is settled, normal tuning can continue without repeating the intervention.

## `README.md`

Document the optional independently versioned repository, the exact pinned revision and the actual skill directory. With a proposed submodule at `skills/KernelBender`, the entry is `skills/KernelBender/skills/kernelbender/SKILL.md`. Register/link that directory through the host's supported skill mechanism or use an explicit path in the prompt. Do not rely on recursive discovery.

If distribution requires notices, preserve the component's actual license in KDA's existing `THIRD_PARTY_NOTICES.md` / `third_party_licenses/` surfaces. Do not choose or assume a license on behalf of the owner.

## What must not change

`kda_experiments` APIs, trusted evaluation inputs, numerical admission policy, profiler collection code, Project Control execution authority and unrelated submodule pins. Candidate hypotheses/design notes use existing task documents and registration text; no new evidence-kind enum or agent controller is needed.

Before merging, use the supplied companion plan to pin an accepted component, run KDA's existing regressions and a task-local consumer walkthrough, and check a conventional request plus a specialized one. Report whether the component is experimentally evaluated, narrowly useful or still provisional; do not market a structural install as proven performance improvement.
