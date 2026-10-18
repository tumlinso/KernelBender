# Delivery validation status

This records the design/bootstrap delivery, not an installed or proven-effective skill.

## Executed in the authoring environment

The package checker validates JSON, task/gate IDs, dependency graphs, safe scoped paths, lane assignment, persisted task-note presence, source-ID references, local links and draft skill format. Its report is `package-check.json`.

The CPU reference script exercises six groups: per-position Boolean full-adder identity; bitplane threshold/tail semantics; linear composition and quadratic observable identities; an explicit intermediate-FP16-rounding counterexample; chronological affine-summary composition; and permutation-compatible elementwise versus changed-axis reduction behavior. Its report is `design-equations.json`.

These are finite CPU algebra/format checks, not GPU implementation, proprietary numerical qualification or evidence that KernelBender improves a model. The half-rounding example demonstrates why an apparently valid real-number reformulation can violate a staged finite-precision contract.

The delivered ZIP is integrity-checked and its contents are bound by `MANIFEST.sha256`. The manifest attests this package only, not external source repositories or future builds.

## Not executed

Native Todo validation/application on the user's installed authority; repository installation or KDA integration; model/design trials; CUDA compilation or sanitizers; GPU timing/profiling; comparisons of skill effectiveness. No user repository, Todo database or submodule was changed. No investigator, skill agent or other agentic Project Control tool was invoked.

## Recheck locally

```bash
python3 scripts/check_package.py --verify-manifest
python3 scripts/check_design_equations.py
```

Both scripts use the Python standard library. The package checker reports structural consistency only. For native intake, use `planning/INTAKE.md`; for actual skill-value testing, use `design/EVALUATION.md`.
