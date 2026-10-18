# Repository guidance

<!-- project-control:start -->
## Project Control workflow

For substantial repository work, use `project-control`. Start with `next_task`,
use `inspect_task` for bounded current-task context, and use `coordinate_task`
for typed synchronization. Rich Project Control reads are secondary escalation
tools when bounded workflow context is insufficient.

Todo Orchestrator remains the transactional authority. First-class Codex agents
receive lanes and roles; local workers are optional bounded children of exactly
one parent claim and never become first-class participants.
<!-- project-control:end -->

KernelBender is an independent repository for an experimental KDA-compatible skill focused on creative GPU kernel design. Its portable instruction/reference skill is implemented. Keep the implementation lightweight and follow the accepted instruction/reference design in `planning/kernelbender-bootstrap/DESIGN.md`. Keep evaluator-only material outside the installed skill and preserve existing KDA/CUDA execution boundaries.

Prefer portable, upstream-compatible work and small reviewable changes. For kernel experiments, check correctness before performance and keep hypotheses, rationale, and measured evidence distinct. Include enough workload, environment, and method detail for others to interpret or reproduce results.

Use `planning/` for project notes. The registered Project Control workspace `kernelbender` and its native Todo authority own task status; use supported operations to inspect or change it. Do not edit Todo's database or generated projections by hand.

Use configured Codex subagents with an explicitly named profile for meaningful delegated engineering. Project Control local workers are observers, not engineering delegates. Preserve existing work and coordinate around concurrent edits.
