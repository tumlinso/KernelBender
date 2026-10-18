# Read-only KDA consumer walkthrough

This walkthrough uses the current KDA prompt and a completed task's own
documents to show where the skill is read and where its design handoff belongs.
It is a format and integration smoke check, not evidence that KernelBender
caused the historical design or improved a kernel.

## Task-local prompt

The existing `prompts/basic-flow.md` asks the agent to inspect the task and
references, then write an implementation-plan draft to `docs/draft.md` before
implementation. For a structural question, the optional invocation sentence
proposed in [KDA-INSERTION.md](KDA-INSERTION.md) goes between those actions:

> For this task's structural merge question, explicitly invoke `$kernelbender`
> before choosing the implementation boundary. Read the task contract and
> existing profile diagnosis first. Put its decision and first discriminating
> experiment in this task's `docs/draft.md`; keep KDA's validator and promotion
> rules unchanged.

## Read set

The smoke read the task-local contract at
`runs/attention-decode-study/workspace/docs/draft.md`, the subsequent measured
diagnosis at `runs/attention-decode-study/workspace/docs/profile-diagnosis.md`,
the KernelBender entry at `skills/kernelbender/SKILL.md`, and its
`references/bridges/parallelism.md` guidance. The historical diagnostic points
to a serialized partial-vector load/merge dependency on the inspected case;
the remaining evidence and per-task numerical contract stay in KDA's own
workspace.

## Design handoff for `docs/draft.md`

**Disposition:** probe a changed merge ownership structure.

**Preserve:** the task's attention operator, required outputs, strict or mixed
numerical track, fixed partial-kernel contract, workload set, and independent
validator. The profile supports a dependent merge path as a hypothesis; low
DRAM throughput does not establish a bandwidth limit.

**Construction:** keep the existing partial kernel and split count. In the
consumer, compute stable split weights once and distribute the partial-vector
features over more participating threads. Compare this combined redesign with
its parent and the strongest measured baseline. The existing attribution
record does not isolate the weight and ownership changes individually.

**First discriminator:** validate every required case under the selected
numerical track, then compare complete resident-operator timing on the same
workload and device. A correctness failure rejects the candidate; a correct
candidate that fails the full-path comparison does not replace the baseline.
Use the task's existing evidence and decision rules; do not modify inputs,
tolerances, or promotion thresholds.

This brief is only a smoke handoff. The historical KDA documents remain the
source of task facts; this repository does not write to that task workspace.
No candidate was registered because this handoff produced no kernel source.
