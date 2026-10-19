# System boundaries as computational resources

Use this page when the cost or correctness boundary crosses SMs, GPUs, the host, a command engine, a virtual address space, or a long-running policy. The design question is which information must cross that boundary, when it must become visible, and which actor can do useful work while it moves. This page supplies constructions and rejection tests; retrieve exact machine contracts from KernelWiki before implementing them.

For a Volta target, retrieve the KernelWiki contracts `hw-volta-vmm-addressing`, `hw-volta-feature-boundaries`, `hw-volta-resources`, and `hw-volta-participation` when the design depends on address views, primitive eligibility, execution resources, or synchronization. KernelBender's [boundary bridge](../bridges/boundaries.md), [ownership bridge](../bridges/ownership.md), [caller questions](../caller.md), and [source locators](../sources.md) help establish the application and provenance side of those contracts.

## Enter through the boundary you need to change

| Problem clue | Construction to examine | Stable Atlas IDs |
|---|---|---|
| A hot counter, queue head, or ownership word is shared by many updates | Reduce within a local group, shard independent destinations, or use a justified associative/idempotent merge | M21, M29, C04, C24 |
| A requester reads many scattered fields owned by another GPU | Compare direct pull, bulk staging, and a compact query answered where the state resides | M34–M35, C20, C23 |
| The receiver already has a valid base state | Send changed positions or support, with a base/epoch identity and dense fallback | C21 |
| A producer and consumer reuse slots asynchronously | Specify reservation, publication, consumption, and reuse as distinct states | M35, C22 |
| A phase boundary uses a stream counter or cooperative launch | Check the public API's own event/order/admission contract and retain ordinary batching as a control | M31–M32, C22, C25 |
| Updates are order-independent and duplicate proposals may collapse | Consider a monotone join over a finite state space, with explicit termination over queued and in-flight work | C24 |
| Many small tasks reuse a compact set of coefficients or layouts | Treat a resident operator palette as a hypothesis and compare its retained state against batching and graphs | C25 |
| A periodic window crosses the end of a ring | Consider two virtual views of one backing allocation, if the public mapping contract permits it | M40, C29 |
| Data needs a fixed format conversion or only a completion update | Check whether a non-SM actor can express that narrow operation; keep public copy/kernel paths as controls | M36–M38, C26–C27 |
| A smooth nonlinear function is expensive and reused over a bounded domain | Consider a legal lookup/interpolation path only with a complete numerical contract and a table-cost comparison | M50, C31 |
| A launch or placement policy changes by workload phase | Select among already-correct choices using a cheap signal and a break-even rule | M42, M46–M47, C30, C32 |
| Useful-byte fraction, host/GPU path, or sustained operating state changes the result | Model memory transactions, page placement, directed topology, shared resources, temperature, and recovery boundaries | M22, M43–M45, M51–M52, C23, C33, C38 |
| A desired instruction or transformation appears only in a binary, driver, or firmware source | Treat that as a research boundary; first find an owned, supported invocation path | M37–M39, M48–M50, C26–C28 |

The IDs preserve provenance to the Circuit-Bending Atlas. They are not hardware authority. KernelWiki and primary sources own exact instruction, memory, access, and synchronization facts. Atlas R06–R10 and R13–R14 provide the source-backed system boundary map; R11–R12 frame complete cost models and evidence scope.

## Keep confidence and reachability independent

Record two judgments for any system-side idea. **Knowledge confidence** describes what the evidence establishes: a documented public contract; behavior reported in implementation source; a bounded observation; a mathematical construction; an untested performance hypothesis; or an unresolved claim. **Reachability** describes who can actually invoke it: ordinary public CUDA; a platform- or device-conditional public path; a driver-owned/private path; or an unknown/privileged frontier. High confidence that a driver emits a command does not make that command a public application interface. A plausible construction can be mathematically clear while its required access remains unavailable.

Do not convert reachability evidence into an execution proposal. Peer access does not imply peer atomics; addressability does not define ordering or progress; a field in a descriptor does not provide ownership rules; a code path for one product does not imply a usable path for another. Keep restricted ideas as research leads until the interface, lifecycle, and recovery contract are established. See Atlas R06–R10 and R13–R14 for the source material behind these distinctions.

## Compare information paths with complete costs

For a remote query over owner-held state, compare three semantically equivalent paths. A useful first-order model is:

```text
pull  = request/setup + remote bytes / effective path rate + requester work
stage = copy/setup    + staged bytes / effective path rate + local reuse work
owner = publish/queue + owner computation + reply bytes / effective path rate
```

These are cost ledgers, not latency predictions. Include synchronization, batching, queue admission, reply handling, owner-side contention, and tail latency. If a prepared representation costs `P` and saves `s` per use for `q` uses, it pays only when `q*s > P + maintenance`; include invalidation and decode in those terms. Direct pull can be best for a small rare query, staging for dense repeated reuse, and owner computation when it sharply reduces returned information. C20 and C23 are candidate constructions, not measured recommendations.

For a dense payload of `n` values, compare `n*w` bytes with a delta containing `k` changed entries of index width `i` and value width `w`: the encoded payload is approximately `k*(i+w)` bytes plus headers. This representation can reduce traffic only when the receiver can apply it to the identified base without paying an equally large reconstruction cost on every use. Compare the measured density against the break-even `k*(i+w) + header < n*w`; include detection, encoding, base maintenance, decoding, and the switch to dense transfer. Define duplicate and ordering semantics. An epoch or base identifier makes stale deltas detectable; it does not by itself make the update protocol correct. This is the design space of C21.

For a cross-actor ring, model each slot as `free → reserved → published(e) → consumed(e) → reusable(e+1)`. The producer owns a reserved slot, writes its payload, and publishes the matching epoch; the consumer reads only after observing that publication and signals reuse only after finishing. Reservation is not publication. Also decide wrap bounds, cancellation, backpressure, shutdown, and what happens when a peer stops. Participation, visibility, and progress must each be proven for the exact interface. A finite stress test can reveal errors but cannot grant a missing memory-model guarantee. C22 is a proof outline, not a universal queue implementation; use the caller's ownership requirements and KernelWiki's exact participation contract.

If updates form a join operation `x ← x ⊔ d` that is associative, commutative, and idempotent, duplicate proposals can merge without choosing one winning order. C24 applies this idea to monotone state propagation, such as accumulating reachability bits. It is relevant only when the state progresses through a finite-height domain (or another convergence argument applies) and the work scheduler eventually processes relevant updates. Count queued and in-flight work during termination detection. Floating addition, overwrite, and general iterative simulation do not qualify merely because they are parallel. Compare duplicate work and hot-target contention against a synchronized frontier or locally aggregated updates.

Retaining reusable state in a resident executor (C25) is a separate scheduling hypothesis. Compare it against proper batching, fused kernels, and graph replay; count queueing, occupancy reserved for service, divergence across the finite operator palette, and stop/drain behavior. It should remain an experiment design until a workload demonstrates that repeated state reload or launch overhead dominates.

## Change an address view without changing the payload

For a ring of `N` elements, a candidate VMM view reserves a virtual interval of `2N` elements and maps the same backing region into both halves. A window of length at most `N` can then be addressed contiguously from a start position in the first half. This changes the address expression; it does not change producer/consumer ownership or publication rules. It is useful only when the actual allocation granularity and mapping permissions allow the view, concurrent alias use has a supported visibility contract, and the consumer accepts the resulting layout.

Compare the full path:

```text
view path = mapping/setup amortized over uses + view walk + translation/cache costs
baseline  = modulo or two-segment walk + its address and branch costs
```

The VMM setup is a phase boundary, not a presumed per-element dispatch. Query the exact public contract and synchronize before changing backing. Preserve a conventional split-window or modulo fallback. For Volta, use `hw-volta-vmm-addressing` and `hw-volta-feature-boundaries` for the exact address, granularity, and eligibility rules; do not infer coherence from successful mappings. ATS and translation-policy zoning are platform-specific leads (M41, M42, C30), not generic consequences of NVLink or VMM.

Atlas E23 reports a bounded comparison in which two fixed aliases beat the tested serial modulo ring walk. The two requested sizes both resolved to a 2 MiB mapping granularity and the same logical domain. The power-of-two mask and two-segment alternatives were not tested, and the measurement does not isolate modulo as the cause or establish concurrent-alias coherence. Treat the result as a reason to test the exact view and workload, not as a general VMM speed claim.

## Ask whether another actor can perform the useful work

Copy engines, launch descriptors, and embedded processors can suggest work outside ordinary SM instructions, but each exposes a narrow and versioned contract. Compare a public asynchronous copy plus shader transform against a candidate fixed record remap; count descriptor setup, transfer size, shared HBM/fabric contention, and SM work. A copy actor is not a general-purpose vector processor. A driver-observed remap does not establish a public arbitrary gather or AoS/SoA conversion. C26 remains gated on an owned interface and an exact expressible layout.

Mapped BAR or GPUDirect memory can put an external actor on the data path, but registration lifetime, ownership, and ordering still need an explicit protocol (M44). A pointer that an external engine can address does not establish when a running kernel may consume its writes. Contexts, IPC, and MPS likewise arrange separate execution/resource domains; they do not merge program semantics or promise fairness (M45). Retrieve the target/version-specific contract before relying on sharing or isolation.

For a completion counter, compare supported stream-memory operations, events, or a small kernel against a command-side update. State what the counter represents, who owns it, how publication is ordered, and which completion boundary it marks. An operation on a semaphore word is not an array reduction. If the only invocation path requires patching live driver-owned state, the idea is not an ordinary CUDA design. C27 is explicitly a restricted research lead. Likewise, dependent QMDs (M39, C28), graphics/media paths (M50), and embedded controllers (M49) need separate access, lifecycle, and recovery proof; exposed structure is not a supported user entry point.

When evidence exists only in a cubin or SASS rewrite, preserve the compiler-produced executable as the control. Validate code, relocation, resource, and dependency metadata before differential execution; then test the target variable-latency conditions. A binary edit that passes a small input sample has not established general legality. Record compiler/driver/target identity and binary hashes. The exact target compatibility and execution route belong in KernelWiki and the source/toolchain record (M48, C39).

A documented CUDA texture path can be explored as one interpolation stage in a bounded smooth function (C31). The mathematical interpolation error is only one term: include sampling, coordinate, filtering, conversion, boundary, and table-construction costs in the application contract. Compare with an established polynomial/library path and a direct arithmetic implementation. Do not assume an inaccessible graphics/media engine is available because related blocks appear in source (M50).

## Adapt policy only when observation pays

Use feedback to choose among a small set of already-correct representations, placements, or schedules; do not put a general optimizer in the hot path. For `q` expected future uses, switch only when:

```text
q * expected per-use saving > observation + switching + repacking + uncertainty margin
```

Use the cheapest signal that predicts the decision, add hysteresis and a minimum residence time, log the reason for each switch, and keep a fixed-policy control. Profiler replay can change the measured workload; clocks, thermal state, and concurrent clients can confound an apparent phase signal. C32 is a policy hypothesis; M42/M46 and C30 describe signals or translation controls whose availability remains platform-dependent.

Special-register identity and clocks can help annotate an observation or distinguish service instances, but they are not portable task IDs, placement controls, or a cross-GPU time base (M47). Retrieve exact target semantics before using them even for a policy.

Power and reliability also belong in the cost boundary. Compare equal useful work after thermal settling, at unchanged operating limits, and include throughput, latency, and energy per result. A lower instantaneous power reading can still mean more total energy. Use health telemetry to identify contaminated runs and define idempotent checkpoint/restart boundaries; do not make correctness depend on speculative reset or fault behavior. C33 and M51–M52 motivate measurements and failure planning, not a schedule winner or hardware modification. C38's empirical conflict map, if a stable one is observed, is only a placement hint; correctness must not depend on an inferred cache-slice or HBM-address hash.

## Preserve the scope of existing observations

Atlas experiment IDs below refer to one campaign and its stated cases. The original experiment protocols include cases that were never run; `GPU_RUN` does not mean every proposed sweep completed. A timing difference is an observation, while its proposed cause is an inference. Include setup, conversion, transfers, and reuse whenever the caller pays them.

- **E16:** six correctness-valid cases compared resident execution, batching, and graph replay for selected task counts and rounds. Resident execution was slower in those cases. Skew, broad resource/occupancy sweeps, starvation, and a general retained-state advantage remain untested; this does not rule out a different operator palette or state-reuse regime.
- **E20:** the run measured selected directed peer-copy paths and CUDA direct-access eligibility for the tested pairs. It did not measure independent link counters, establish each physical route or saturation, test multi-stream saturation, or test concurrent owner compute. Do not generalize the pair-specific rates to a topology rule.
- **E23:** see the fixed-view limitations above. The tested serial modulo baseline was the comparison; the planned working-set range, power-of-two mask, and two-segment baselines were not covered.
- **E25:** under the known synthetic phase schedule, adaptive observation cost dominated the selected cases. The offline oracle was in-sample and excluded calibration by construction; no online-policy win or general regret result was established.
- **E27–E30:** remain `NOT_RUN` for their restricted hypotheses. E27 did not invoke the component remapper; E28 did not exercise low-level semaphore-word commands; E29 did not run a QMD dependency; E30 did not execute an edited cubin. Nearby public copy, graph, launch, or PTX/source tests do not validate these restricted operations.

Use the corresponding Atlas IDs when following provenance and the claim-limits and interpretation guidance. Do not turn a missing result into evidence of impossibility, or an adjacent result into evidence for an untested mechanism. For a new candidate, state the strongest conventional baseline, the full cost boundary, the exact access gate, and the smallest falsifier before implementation.
