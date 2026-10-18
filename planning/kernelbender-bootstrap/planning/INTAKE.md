# Safe native Todo intake

The `kernelbender` workspace is already registered with a native Todo authority. Its previously inspected bootstrap root is `/home/tumlinson/KernelBender`; resolve the currently registered checkout instead of assuming a path if it has moved.

Copy this **complete** package to `planning/kernelbender-bootstrap/` in that checkout. Do not blindly copy `draft/` over existing canonical files. The component tasks adopt the drafts selectively into `skills/kernelbender/`.

The plans use native Todo schema v3 and fields inspected in `src/todo_orchestrator/plan.py` and `gates.py`. Acceptance requirements and input references are in persisted task `notes`, not an invented completion-contract field. The source CLI tests confirm:

```bash
PLAN="$(pwd)/planning/kernelbender-bootstrap/planning/kernelbender.todo-plan.json"
project-control plan validate --project kernelbender --file "$PLAN"
# Review valid=true, would_add/would_modify, existing IDs, current work and scope.
project-control plan apply --project kernelbender --file "$PLAN"
```

The apply command is shown for the eventual authorized implementing agent; **it was not run during package preparation**. The read-only Project Control connector does not expose native validation/application. Use the installed authority and normal task lifecycle. If the CLI version differs, inspect its local `plan --help` and preserve native semantics. Do not install a replacement authority, reset a database, clear claims, silently overwrite matching IDs or edit generated projections to make the plan apply.

The plan has seven task-owned outcomes and one aggregate. Its manual gates require review of actual acceptance evidence, not merely file existence. The small command gates name tests that implementation will create. Before GPU work, bind actual execution gates with the current controller/toolchain through supported native operations; the package does not invent site-specific paths or weaken quiescence and numerical checks.

## KDA companion plan

After KB-07 provides an accepted component commit and status, copy the relevant complete package to `planning/kernelbender-bootstrap/` in the independent KDA checkout (or otherwise preserve all referenced inputs there). Then validate/apply the companion using `--project kda` and `planning/kda-integration.todo-plan.json`.

Do not run that companion early. Its readiness is a reviewed cross-repository handoff, not a dependency on an unregistered local `KB-*` task. It owns only a narrow pin/prompt/docs/consumer-test change, not the evaluator or other skill ports. A no-change/experimental outcome is legitimate when the component evaluation does not support default adoption.

## What this delivery validates

Local package checks cover parseability, unique IDs, dependency graphs, safe paths, gate scopes, source IDs, links and draft format. They do not substitute for native Todo validation, model evaluation, actual KDA integration, GPU correctness or measured effectiveness. See `validation/STATUS.md` for the actual executed checks.
