# Candidate-visible evaluation inputs

This tree contains only the shared inputs intended for an A/B design or
implementation attempt. It includes task contracts, probe prompts, public input
cases and seeds, and corrected baseline sources. It contains no review
rubric, oracle implementation, generated holdout values, or results from either
arm.

For a trial, give both arms the same immutable copy of this tree and the same
KDA/CUDA/KernelWiki/NCU/Atlas sources. Arm B additionally receives the pinned
`skills/kernelbender/` installation. Record the copy's SHA-256 manifest with
the trial. Do not give either arm a full KernelBender checkout containing the
evaluator-only tree.

This directory separation is packaging, not access control. A host running
agents and evaluators must enforce access with an isolated account, container,
or equivalent mount policy that exposes the candidate bundle and a narrow
evaluation interface while withholding `evaluation/private/`. The current
shared-agent environment does not establish hostile-agent isolation; without
an enforced boundary, record probes as unblinded and make no holdout-blindness
claim.

The design probes are independent prompts. The native task packets state the
public operation, inputs, outputs, target, numerical rules, and candidate ABI.
The task runner and trusted validation path are prepared separately by the
evaluator. A design brief is not a KDA candidate or a performance result.
