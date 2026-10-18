# Native task: periodic two-bit transition

## Operation

At each step, every site `i` reads the **old** state at `i`, the **old** state
at `(i-1) mod N`, and its mask byte. The new state is
`rule[(state[i] * 4 + state[(i-1) mod N]) * 2 + mask[i]]`. State and rule
entries are bytes in `0..3`; mask bytes are `0` or `1`. All sites update
synchronously. Repeat the same rule and mask for `T` steps. Return the complete
final state and the number of sites whose final state equals `3`.

The byte-per-site public API is in `candidate_api.h`. Input state and mask,
rule table, final state, and count pointer are device addresses. Inputs do not
alias outputs. The function must not retain state between invocations. The
rule and mask may differ on the next invocation. All output elements must be
written. The task's only cases are those in `cases.json`; held-out cases are
created and checked separately by the evaluator.

The candidate may change the internal representation, but must account for
conversion at both API boundaries, periodic wraparound, word/tile tails,
temporary state, and every step of the epoch. No intermediate state is
requested.

## Workloads and objective

Cases cover all 32 possible local tuples, an odd sub-warp length, a multi-step
odd tail, a full-word-scale workload, and a large non-aligned tail. The exact
case list and seeds are in `cases.json`. The primary timing is full epoch
latency per call; memory use is reported separately. Correctness requires
exact byte equality for every final site and the aggregate count.

The baseline uses one conventional scalar-per-site CUDA kernel per step and a
final aggregate pass. It is a valid reference point, not a performance claim.
