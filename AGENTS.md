# Repository guidance

<!-- project-control:start -->
## Project Control and native Todo workflow

Use Project Control's `overview`, `search`, `delta`, `frontier`, `history`,
`evidence`, and `impact` tools for registered-workspace context. They are not
the Todo transaction API. For Todo state and workflow, use the native `todo_*`
tools exposed by the host. Start with `todo_read_authority`; for plan changes,
call `todo_preview_plan`, inspect the returned preview, then pass that exact
preview to `todo_commit_plan` with an idempotency key. Use the corresponding
`todo_open_run`, `todo_create_workspace`, `todo_dispatch_attempt`, outcome,
verification, and recovery tools for later lifecycle steps.

Arguments use a registered workspace ID and, when necessary, an optional
registered `repository` alias. The host binds authority, identity, credentials,
profile, and providers; never pass filesystem roots or bearer credentials as
selectors. Read migrated history with `todo_search_legacy_history`, current
status with `todo_read_legacy_current_tasks`, and preserved declarations with
`todo_read_legacy_project_context`. Imported completion is a source assertion,
not native verification; unknown legacy effects require attention and are never
replayed automatically. Project Control's existing non-Todo tools remain
available for their own purposes.
<!-- project-control:end -->

KernelBender is an independent repository for an experimental KDA-compatible skill focused on creative GPU kernel design. Its portable instruction/reference skill is implemented. Keep the implementation lightweight and follow the accepted instruction/reference design in `planning/kernelbender-bootstrap/DESIGN.md`. Keep evaluator-only material outside the installed skill and preserve existing KDA/CUDA execution boundaries.

Prefer portable, upstream-compatible work and small reviewable changes. For kernel experiments, check correctness before performance and keep hypotheses, rationale, and measured evidence distinct. Include enough workload, environment, and method detail for others to interpret or reproduce results.

Use `planning/` for project notes. The registered Project Control workspace `kernelbender` and its native Todo authority own task status; use supported operations to inspect or change it. Do not edit Todo's database or generated projections by hand.

Use configured Codex subagents with an explicitly named profile for meaningful delegated engineering. Project Control local workers are observers, not engineering delegates. Preserve existing work and coordinate around concurrent edits.
