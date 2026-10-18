# Proposed KDA consumer hook

This is the narrow proposal for the separate KDA integration task. The current
KDA source remains unchanged.

In `prompts/basic-flow.md`, insert an optional paragraph after contract and
workspace inspection, before the existing `docs/draft.md` planning step:

> When the task has meaningful specialization, composition, representation, or
> reuse freedom—or the caller explicitly asks for a structural rethink—invoke
> `$kernelbender` before committing the design. Use its concise decision and
> first discriminating experiment in the existing `docs/draft.md`. A
> conventional/library route remains valid. A new design does not need a
> profile; use existing profiling evidence for an implemented hotspot. Keep
> task semantics, numerical requirements, and KDA validation authoritative.

Register the skill through the host's supported skill path when the accepted
KernelBender revision is pinned. The nested entry path will be
`skills/KernelBender/skills/kernelbender/SKILL.md`; do not depend on recursive
skill discovery. An explicit path read from a local checkout is suitable for a
task-local pilot.

In `docs/agent-flow.md`, add one sentence linking the skill for a later
structural re-entry when evidence or the caller's output, reuse, or target
constraints expose a different design question. In `README.md`, document the
optional independent repository and exact submodule pin/path. Do not add
`kda_experiments` fields or change trusted task inputs, evaluation policy,
profiling code, or execution controls.

The handoff stays in `docs/draft.md`; a design paragraph is not a candidate.
Only after implementation exists should the current CLI register a real source
directory and manifest with its existing `--hypothesis`, `--change`, and
optional `--parent` arguments. Its available evidence kinds remain `profile`,
`sass`, and `ablation`.
