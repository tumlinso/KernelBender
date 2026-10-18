# Component package and KDA consumer results

## Package

The portable runtime unit is exactly `skills/kernelbender/`. The CPU contract
test stages this directory under an isolated temporary `CODEX_HOME/skills/`
layout, compares the installed file set with the source, and checks that no
repository evaluation, test, or planning material enters that staged package.
The stage is deleted with the test's temporary directory. No host-global skill
installation was made.

`SKILL.md` declares the name `kernelbender` and routes specialized structural
design while excluding ordinary CUDA help, profiling, and KDA evaluation.
The skill-creator `quick_validate.py` check passed. The checked-in CPU tests
also cover frontmatter identity/routing, all local Markdown links, and every
cited source key's locator.

## KDA consumer

The read-only walkthrough is in [integration/kda-consumer-smoke.md](../integration/kda-consumer-smoke.md), with the separate change proposal in
[integration/KDA-INSERTION.md](../integration/KDA-INSERTION.md). It follows the
current KDA `prompts/basic-flow.md` contract: inspect the task and references,
then put the design draft in the task's existing `docs/draft.md` before
implementation.

KDA checkout inspected: commit `b430320a850c95238c8e30bc95e8f077f67c8bd1`.
Its `skills/KernelBender` gitlink is still at bootstrap commit
`cf14dd845244039da343c44632bd188a82bc7b0e`, which does not yet contain the
skill entry. For the local walkthrough, the source entry was read directly
from this component checkout. The eventual nested path after a separate KDA
pin update is `skills/KernelBender/skills/kernelbender/SKILL.md`.

The existing CLI was invoked read-only with `python3 -m kda_experiments --help`,
`python3 -m kda_experiments register --help`, and
`python3 -m kda_experiments attach-evidence --help` from the KDA checkout.
`register` takes an actual `SOURCE_DIR`, `--manifest`, `--hypothesis`, and
`--change`, with optional `--parent`, `--baseline`, and `--experiment-group`;
`attach-evidence` supports only `profile`, `sass`, and `ablation`. The task-local
brief is documentation, so it is not registered as a candidate or as a new
evidence kind. Candidate registration is deferred until real source exists.

The source contract is visible in `kda_experiments/cli.py` (the `register` and
`attach-evidence` argument definitions) and `kda_experiments/contracts.py`
(`read_candidate_manifest`, which requires a non-empty list of relative files).
The task prompt and draft locations come from `prompts/basic-flow.md` and
`docs/agent-flow.md`; no new engine field is needed.

No KDA source or task workspace was changed. The prompt insertion, re-entry
link, README mention, and exact revision/path update remain for the separate
KDA integration task after component acceptance.

## Activation scope

The directory staging test establishes an isolated `CODEX_HOME/skills/kernelbender`
install layout and frontmatter discovery identity. This session did not mutate
the active Codex host registry or make a live `$kernelbender` model invocation;
the current KDA submodule pin also predates the skill. The demonstrated local
consumer explicitly read the component entry by path. A live registered
invocation should be verified after the accepted pin is installed through the
chosen host's supported mechanism.
