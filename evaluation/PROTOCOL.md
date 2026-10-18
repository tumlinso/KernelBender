# Frozen evaluation protocol v1

This protocol freezes the candidate-visible tasks and trusted acceptance rules
for the initial KernelBender pilot. It records an evaluation setup, not an
effectiveness result. No model trial, GPU validation, sanitizer run, or timing
has been performed for this protocol version.

## Candidate-visible material

The six independent prompts in `candidate/probes/` cover demanded output,
packed per-position state, reuse and invalidation, architecture reachability,
evidence-led experiments, and an ordinary dense-library control. Give both
arms the same immutable copy of `evaluation/candidate/` and the same KDA,
CUDA, KernelWiki, ncu-report-skill, and Circuit-Bending Atlas access. Arm B also
receives the pinned `skills/kernelbender/` installation. Start each attempt in
a fresh context; neither arm receives the other arm's design or results.

The candidate bundle includes the public contracts, cases and seeds, API
headers, and corrected conventional CUDA baselines. It excludes
`evaluation/private/`, generated holdout inputs, evaluator results, and other
arm artifacts. Generate its SHA-256 manifest with
`evaluation/private/stage_candidate_bundle.py` and retain that manifest with
the trial record. The evaluator loads candidate code only from the immutable
KDA snapshot; candidates cannot supply the reference, holdouts, or timing
policy.

Trial packaging must enforce the boundary with mounts or an equivalent access
policy. The verified shell wrapper uses a bubblewrap namespace exposing the
public bundle and shared sources read-only, a private candidate work area, no
repository/evaluator/other-arm mounts, no network, and no GPU during design
probes. This constrains commands sent through that wrapper; it does not prove
hostile-agent isolation from every model tool. Do not describe the runs as
blind if contexts can obtain private material through another route.

## Native tasks

All three native tasks use the KDA v1 task interface and corrected baselines
under `candidate/native/`. Compile for CUDA 12.9 `sm_70` and the admitted V100.
Public shapes and seeds are fixed in each `cases.json`; do not shrink or drop a
case after seeing a candidate result.

| Task | Public workload | Acceptance |
| --- | --- | --- |
| `kb-native-bool-transition-v1` | `N=32,T=1` truth-table coverage; `N=31,T=1`; `N=33,T=8`; `N=1024,T=32`; `N=65537,T=8` | Exact synchronous periodic transition, complete final byte state, and exact count of state-3 sites. |
| `kb-native-observable-energy-v1` | `(B,K,M,U)=(1,32,256,1)`, `(8,96,1024,1)`, `(8,96,1024,64)` | Every squared response energy within `2e-4 + 5e-5*abs(reference)`, using binary64 over represented FP32 inputs. All query uses and preparation/update work count in the epoch. |
| `kb-native-dense-gemm-control-v1` | `(M,N,K)=(512,512,512)` and `(1024,384,256)`, with declared alpha/beta | Full row-major `C=alpha*A*B+beta*C` output within `2e-5 + 5e-5*abs(reference)`. cuBLAS is the conventional incumbent and may remain selected. |

The energy baseline flattens the supplied `U*B` rows into one cuBLAS SGEMM
before squared-row reduction, so it batches every use available to a candidate.
The private checks add changed weights in the same process, a wide/small-batch
case, and zero/cancellation/small-scale guards. Boolean holdouts exercise a
long epoch with a tail and a changed mask/rule. The GEMM holdout is ragged and
rectangular. Holdout values and seeds remain under `evaluation/private/` and
are not part of this protocol or the candidate bundle.

## Measurement and execution

The primary metrics are full Boolean epoch latency, complete energy update
epoch latency, and full dense operator latency. Candidate inputs are resident.
Each benchmark restores dense C and poisons Boolean/energy outputs before every
invocation, outside the timed interval. Validation after every warmup and
sample compares fresh output to the independent reference. Timing includes the
candidate call and full-device completion synchronization; it excludes host
input preparation/copies and dense C restoration. Candidate allocation,
packing, preparation, all epoch uses, and output extraction remain candidate
costs.

The frozen KDA policy is two warmups, three samples per round, two rounds, and
two confirmation rounds. Promotion requires at least 2% improvement, allows at
most 10% regression, uses 95% confidence and 1,000 bootstrap samples, and
minimizes the declared latency metric. Per-task limits are eight candidates,
one build job, and 900 seconds. These are measurement repetitions and search
limits, not independent model trials.

The site task manifests bind the existing CUDA controller launcher, runtime
identity, CUDA controller script, CUDA 12.9 compiler and libraries, corrected
baseline, public API, independent references, and holdouts as trusted inputs.
GPU probe, validation, memory/race sanitizer, and timing actions require the
separate controller-backed KB-06 gates. Before the first A/B implementation
attempt, freeze the model/version/settings, per-agent time and tool-call
budgets, candidate/build cap, GPU lease budget, and trial order in the run
record. Give both arms the same limits and count failed attempts and profiling
costs.

## CPU preparation evidence

The independent reference and contract checks are in
`tests/test_evaluation_contracts.py`. The current source passed 16 tests. The
three current-hash KDA task manifests and fresh baseline preparation receipts
were verified with `register` and CPU-only `prepare` before any GPU action;
their host-bound copies and KDA workspaces are generated outside this portable
repository. Those receipts prove schema acceptance and compilation only, not
candidate correctness on a device or performance.
