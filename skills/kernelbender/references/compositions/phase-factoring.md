# Composition: factor the hot phases of a large circuit

**Use when:** an all-in-one kernel has a concrete problem—excess live state, code footprint, too few runnable tasks, expensive synchronization, or a cold/rare path inflating the common path. The goal is to choose phase boundaries jointly with representation, while retaining a strong conventional schedule.

## Make dependencies composable before splitting

If a sequence appears serial, ask whether each segment has a compact summary with an associative composition law. An affine segment `x' = A*x+b` can be summarized by `(A,b)`; applying segment 1 then 2 gives `(A2*A1, A2*b1+b2)`. This creates a possible parallel-prefix structure only when inputs are known and summary construction/merge costs are less than the original sequence. A nonlinear, coupled or data-dependent recurrence cannot become affine by relabeling it. Reassociation may also alter finite-precision results.

For a reduction with a small mergeable sufficient statistic, hold that state per tile and merge summaries instead of writing every intermediate. For online normalized exponential aggregation, one example summary is `(m,l,u)` where `m` is local max, `l` is the shifted exponential sum and `u` its weighted numerator; merging rescales both summaries to their combined maximum. Empty or masked tiles need explicit rules. If every partial value is observable, the summary may no longer implement the caller's output. (Atlas R11, R15; C12, C34.)

## Split common, rare and resource-heavy work

Separate a small frequent phase from a large but uncommon transform or fallback. Preserve encoded state through the hot loop; route only exceptional cases to a general path. Alternatively, distribute independent groups into partial results and add one valid merge phase. A phase boundary trades code/live-state and scheduling pressure for stores, reloads, dispatch and synchronization. Write these terms before changing the kernel boundary.

The same principle applies to operand streams. Interleave required independent work that can use otherwise idle dependency slots, but do not add “useful-looking” work absent from the baseline. Register-source reordering or an amortized operand copy is only a candidate when a concrete instruction-read bottleneck is established. Keep binary/cubin transformation and driver controls as research work with their own source, access and validation boundaries. (Atlas M12, M13, M16, M17, M19; C17–C19.)

Persistent state is a separate choice from a good phase decomposition. A bounded resident service could reuse a small operator palette, but needs a finite stop/drain protocol, enough resources for its producer, skew handling and progress guarantees. It must be compared with proper batching and graph replay; no scheduler or hidden background execution is part of this skill. Atlas E16 found its measured resident path slower than batching and graph replay for the selected cases; this is a useful rejection example, not a universal ban. (Atlas M15, M30, M33; C25, C34.)

## Search over formulations, not only launch parameters

An efficient investigation can generate a short list that changes a structural choice: observable output, state representation, ownership map, algebra, reuse boundary or phase partition. For each option write the full path cost and the best conventional alternative. Drop candidates that violate semantics or require an unsupported mechanism before compiling; preserve a plausible candidate until a small falsifier can decide it. Parameter tuning within one family can then occur through the existing implementation/evaluation workflow.

This card does not propose a new search engine or optimizer. Its handoff is a concrete design brief: selected construction, equation, real invariant, format/owner through each phase, hidden costs, strongest alternative, first semantic test and first measurement that would change the choice. (Atlas C34, C39.)

## Validation and boundaries

For an algebraic summary, test segment composition and output states against a sequential oracle across boundary lengths, masked segments and adversarial numeric values. For a pipeline, count all transfers, barriers, graph capture/setup, dispatch and tail completion that the caller pays. Prove participant scope, payload visibility and progress separately. Use `hw-volta-participation` on Volta; do not use Ampere `cp.async`, Hopper TMA or cluster semantics in a Volta schedule. Use `hw-ampere-async-copy` only for exact `sm80` eligibility and wait/barrier rules.

Reject a split when the inserted boundaries dominate, a source's data is no longer available, output observability prevents summarization, or the producer can be starved by the resident consumer. Retain native monolithic, library, batching and graph-replay controls where they fit the work.

Atlas IDs: M12–M20, M30, M33; C17–C19, C25, C34, C39; E02–E04, E06, E15–E16, E30, E32, E39. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
