# Repository guidance

<!-- project-control:start -->
## Project Control and Todo workflow

Use Project Control's existing `overview`, `search`, `delta`, `frontier`, `history`,
`evidence`, and `impact` reads for registered-workspace context and migrated Todo
status/history. The compact profile catalogs are observer 11, coder 12, and
mutator 16 tools. Routine workflow begins with
`next_task(project, repository?, task_id?, run_id?)`; pass its returned handle to
`inspect_task`, `coordinate_task`, and `finish_task`. Use the live host manifest
for exact schemas and profile permissions.

Project Control binds workflow handles to the registered workspace, identity,
profile, credentials, and providers. Routine agents should not manage native
Todo IDs, leases, credentials, or retry keys, and do not pass raw repository
paths as selectors. Privileged plan changes, execution maintenance, and project
metadata stay on their established routes. Observer reads need no task claim and
cannot mutate. The standalone Todo API and CLI remain available for separately
managed authorities. Imported completion is a source assertion, not native
verification; unknown legacy effects require attention and are never replayed
automatically. Existing non-Todo tools remain available for their own purposes.
<!-- project-control:end -->

KernelBender is an independent repository for an experimental KDA-compatible skill focused on creative GPU kernel design. Its portable instruction/reference skill is implemented. Keep the implementation lightweight and follow the accepted instruction/reference design in `planning/kernelbender-bootstrap/DESIGN.md`. Keep evaluator-only material outside the installed skill and preserve existing KDA/CUDA execution boundaries.

Prefer portable, upstream-compatible work and small reviewable changes. For kernel experiments, check correctness before performance and keep hypotheses, rationale, and measured evidence distinct. Include enough workload, environment, and method detail for others to interpret or reproduce results.

Use `planning/` for project notes. The registered Project Control workspace `kernelbender` and its native Todo authority own task status; use supported operations to inspect or change it. Do not edit Todo's database or generated projections by hand.

Use configured Codex subagents with an explicitly named profile for meaningful delegated engineering. Project Control local workers are observers, not engineering delegates. Preserve existing work and coordinate around concurrent edits.
