# Evaluate added design capability, not clever prose

## Questions to answer separately

1. Does the skill activate and return useful, bounded guidance?
2. Does it produce feasible, structurally different designs that the existing competent workflow misses?
3. Under an equal overall budget, do those designs yield a better correct implementation or another declared objective?

A passing link/schema test answers none of questions 2–3. The historical attention improvement predates KernelBender and is a teaching example, not its treatment result. Reproducing a card verbatim shows access/recall, not broad invention.

## Baseline and treatment

**A — current competent stack.** Same model/version/settings, KDA loop, KernelWiki, ncu-report-skill, CUDA skill including `machine-aligned-design.md`, Atlas access, source/tool access and trusted evaluation contracts. Give A the same opportunity to step back and spend its budget. Do not compare to a bare one-shot CUDA prompt.

**B — A plus KernelBender.** Load the candidate skill as the additional intervention. Match wall-clock/model-token/tool-call/GPU budgets as practical and record actual costs separately. More documentation and time are part of the intervention's cost, not free treatment resources. No higher-reasoning model in only one arm.

A third **material-only ablation** is optional on one informative task after a benefit is observed: provide the same relevant bridge substrate to the current CUDA method, without the new KernelBender procedure. This tests whether the added value is the material, the reasoning guidance or their interaction. It is not a mandatory three-arm benchmark over every problem.

Use fresh independent design/implementation contexts. Do not give A B's design or let the second arm inherit the first arm's discoveries. Counterbalance execution order and share only the task's legitimate sources and corrected baseline artifacts. Names/settings are fixed at execution, not invented in this package.

## Stage 1 — six small design probes

Use `evaluation/scenarios.json` to cover output demand, reuse/invalidation, packed per-position state, numerical boundaries, architecture/access transfer and an ordinary-library control. Review the briefs for operator fidelity, actual construction, legitimate specialization, complete cost, structural diversity and quality of the next experiment.

Keep review evidence behavioral: quote the concrete design/omission and classify it, rather than assign an unexplained “creativity score.” A human or qualified independent reviewer checks consequential mathematical/hardware claims. Model self-ratings may help triage but cannot establish correctness or novelty. [IDEAS, SELFCORRECT]

Use a few paired fresh contexts and vary a decisive condition: required full intermediate versus final statistic, fixed versus frequently updated parameters, packed input versus forced scalar output, and available versus unavailable target mechanism. The correct answer need not always change algorithm, but it should respond to the changed reason.

Mandatory failures to catch: hidden benchmark-value specialization; silent numerical relaxation; invented native support; ignored output/initial/final state; omitted representation costs; profiler replay treated as a speedup; or a required restricted API treated as public. Good conventional routing is positive evidence on the control.

Do not count tile-size variants as distinct design families. Do not reward novelty when the conventional answer is superior. Freeze the draft after a small development pass before starting the native pilot; a major revision requires declaring a new version and separating earlier results.

## Stage 2 — a bounded implementation pilot

Use two specialized task families and one conventional control, prepared by the evaluator from the scenario templates. The candidate skill must not see evaluator answer notes, generated holdout cases or results from the other arm. Its published examples remain available to both arms through their legitimate source access; do not claim unseen novelty when a solution is directly taught.

Suggested families:

- A **reused categorical/Boolean pipeline** with a specified transition or per-position threshold operation, real input/output representation and update epochs. Include tails and a case where encoding cannot be amortized. This tests non-tensor computational substrate.
- A **composed numerical operator with a small demanded output**, immutable or updateable parameters and an explicitly allowed numerical contract. Include a strict-intermediate variant as a semantic guard, not a benchmark loophole. This tests consumer/lifetime reformulation and conventional fallback.
- A **well-served dense-library control**, with no hidden structure or changeable intermediate semantics. This tests whether the skill adds unnecessary work or replaces a strong baseline with novelty for its own sake.

Prepare actual task code/independent references in the task workspace; this package supplies specifications, not uncompiled kernels pretending to be benchmarks. Reuse the KDA task format and launcher. Each arm receives the same contract, corrected valid baseline and independent evaluation opportunity. Use a validation set containing non-performance guards and held-out represented inputs. Do not permit candidate edits to trusted references or timing drivers.

Start with one paired A/B implementation attempt per family: six independent sessions. Repeat an independent paired attempt for any claimed skill-level win or result sensitive to generation variability, up to one additional pair per family in this initial pilot. This is a bounded pilot, not a statistically powered general superiority claim. Record model/agent variability separately from repeated GPU timing samples; hundreds of timing samples from one generated kernel are not hundreds of independent design trials.

Before running, fix a per-attempt model/effort budget, candidate/build cap and admitted GPU budget using the existing operator/hardware environment. Count failed attempts, profiling and correctness costs. No hidden extra polishing for B. If a task is impossible or its environment unavailable, record it and repair the evaluator equally; do not silently drop the hardest case or shrink workloads after OOM.

## Outcome measures

Primary: best *valid* delivered implementation under the allotted search budget, evaluated on the caller's complete objective with independent held-out checks. A baseline retained after no successful new candidate is an outcome, not missing data. Incorrect/noncompiling candidates cannot receive performance credit.

Secondary: feasible distinct design families, useful reformulations, unnecessary complexity, number/cost of experiments, time to a valid design, quality of causal questions and conditional adaptation. Capacity savings are reported separately unless the task's objective explicitly values them.

KDA's ordinary paired timing and promotion rules qualify individual kernel improvements. At the skill level, report per-task/per-attempt results and uncertainty across independent agent attempts. Do not pool unrelated numerical contracts or architectures into one attractive mean. A small pilot can establish local usefulness or a failure mode, not universal creativity.

## Adoption decision

**Retain the full skill** when it demonstrates useful design behavior and a measured advantage or a documented reduction in engineering cost on the specialized tasks without breaking semantics or materially harming the control. State how narrow the support is.

**Simplify to the substrate/route** when new material helps but the added procedure does not outperform the existing method.

**Restrict activation or keep experimental** when benefits are narrow or generation-dependent.

**Do not promote an effectiveness claim** when no incremental benefit is observed. Structural implementation may still be complete and the pilot honestly `evaluated_not_promoted`; do not turn that into another epic of benchmark work.

One failed implementation should not blacklist a representation family. Conversely, one spectacular lucky kernel is insufficient to declare a generally better design method.
