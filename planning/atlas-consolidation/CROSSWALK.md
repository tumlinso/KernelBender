# Atlas claim-level migration crosswalk

Source identity for every ID below is standalone Atlas revision
5b5629b001da4a42d6f41a84d94f73c07a29d478. The row destination is a
responsibility split, not permission to copy the Atlas text. KernelBender
contains original synthesis and construction logic. KernelWiki owns exact
hardware contracts and bounded experimental claims. Items not yet backed by a
dedicated Wiki page remain at the pinned Atlas source and are marked as gaps.

Local Atlas cards can be retrieved without relying on a public URL, for example:

    git -C /home/tumlinson/gpu_circuit_bending_atlas show 5b5629b001da4a42d6f41a84d94f73c07a29d478:mechanisms/M06.md

## Atlas references R00–R15

| ID and subject | KernelBender design ownership | KernelWiki fact/evidence ownership or retained gap |
|---|---|---|
| R00 Reading and evidence contract | references/experiments.md and sources.md: separate hypothesis, mathematical construction, source fact, and measurement. | Atlas campaign source record plus hw-volta-atlas-evidence-index owns campaign provenance/status. |
| R01 Machine reference | architecture.md routes by exact target; designs do not restate capacities. | hw-volta-resources and architecture-specific pages own enabled product facts; CUDA skill remains the broader cross-generation source. |
| R02 Execution, scoreboards, operands | affordances/operand-flow.md turns dependency and operand paths into design questions. | hw-volta-operand-delivery and hw-volta-resources own bounded source-backed Volta facts; timing is not an ISA bank-allocation guarantee. |
| R03 Memory as algorithmic structure | system-boundaries.md and ownership-fragments.md use information location, lifetime, and representation as design inputs. | hw-volta-resources and hw-volta-vmm-addressing own relevant contracts; broad translation/cache details not separately migrated stay in Atlas/primary sources. |
| R04 ISA families and generation traps | architecture.md and system-boundaries.md require exact-target checks before design selection. | hw-volta-feature-boundaries, hw-volta-mma, plus hw-ampere-async-copy, hw-ampere-tensor-operations, and hw-ampere-memory-resources own the migrated boundaries. PTX spelling does not imply native support. |
| R05 Tensor geometry/native register interfaces | compositions/tensor-circuits.md interprets MMA as candidate small bilinear constructions. | hw-volta-mma and hw-volta-atlas-e09-mma-coordinate own exact explicit PTX map and bounded map check; technique-volta-fragment-layout owns implementation examples. Raw WMMA lane ownership remains unestablished. |
| R06 Participation, visibility, progress | system-boundaries.md makes all three proof obligations explicit for a proposed protocol. | hw-volta-participation and hw-volta-numerics own exact collective, ordering, scope, and numerical constraints; E15/E16 remain bounded campaign evidence. |
| R07 NVLink, PCIe, NUMA boundaries | system-compositions.md proposes owner compute, support/delta transfer, and topology-aware alternatives. | Pair-specific source facts remain in Atlas sources and evidence E18–E21. A complete KernelWiki topology/NUMA contract page remains a gap; rates are not generalized. |
| R08 Virtual memory, ATS, faults | system-boundaries.md treats address views and migration policy as separate design hypotheses. | hw-volta-vmm-addressing owns public VMM mapping/access/granularity facts; ATS/fault details not separately paged remain at Atlas source IDs. E23 is narrowly bounded. |
| R09 Non-SM command machine | system-boundaries.md preserves copy-engine and descriptor ideas only as reachability-gated leads. | hw-volta-feature-boundaries records public/restricted boundaries; source-only driver/class facts are not CUDA invocation contracts. E27–E29 are NOT_RUN. |
| R10 Toolchain and binary evidence | system-boundaries.md keeps binary rewriting out of ordinary design prescriptions. | hw-volta-feature-boundaries and versioned KernelWiki source records own compatibility; E30 is NOT_RUN and does not establish an edit path. |
| R11 Complete performance model | opportunity-index.md, affordances, and compositions compare the full caller-visible region, including preparation, reuse, conversion, and extraction. | KernelWiki owns target-specific resource/cost facts; E39 is a bounded comparator, not a general recommendation. |
| R12 Measurement discipline/observability | experiments.md requires a falsifiable discriminator and preserves unmeasured hypotheses. | hw-volta-atlas-evidence-index routes scoped summaries; measurement tool contracts remain with ncu-report-skill and primary profiler documentation. |
| R13 Electrical, firmware, reliability frontier | system-boundaries.md labels platform/firmware ideas as research leads, not implementation affordances. | Exact software-visible claims remain in source records; no schematic, hidden engine, or firmware access is inferred. Dedicated coverage remains a gap. |
| R14 Composition, conflict, scope | opportunity-index.md and system-boundaries.md compose mechanisms while exposing shared bottlenecks. | KernelWiki owns each exact architectural contract; no Atlas composition is copied as an authoritative machine fact. |
| R15 Numerical contracts | arithmetic-tensor.md and screening-refinement.md require range, error, and observable-result proofs. | hw-volta-numerics and Ampere tensor-operations own target-specific forms; E10 is finite test evidence, not a universal error bound. |

## Mechanisms M01–M52

| ID and computational affordance | KernelBender construction home | KernelWiki factual lane / evidence boundary |
|---|---|---|
| M01 LOP3 Boolean circuits | affordances/bit-routing.md; compositions/discrete-state.md and arithmetic-circuits.md | hw-volta-integer-routing owns exact Boolean instruction semantics; hw-volta-feature-boundaries only records target boundaries. Official PTX remains primary. |
| M02 Mask rank/select | compositions/positional-routing.md and screening-refinement.md | hw-volta-integer-routing owns exact __fns contract; abstract rank/select algebra does not emulate the API. CUDA Integer Intrinsics is primary. |
| M03 PRMT register lookup | compositions/positional-routing.md | hw-volta-integer-routing owns exact byte permutation forms; hw-volta-feature-boundaries is not the instruction contract. Official PTX/CUDA docs remain primary. |
| M04 Shuffle routing | compositions/positional-routing.md and discrete-state.md | hw-volta-integer-routing owns exact shuffle forms; hw-volta-participation owns participant constraints. |
| M05 Match as local associative table | compositions/positional-routing.md | hw-volta-integer-routing owns exact match API semantics; hw-volta-participation owns warp collective scope; E05 is selected routing evidence only. |
| M06 Ballot transpose/bit-sliced state | affordances/bit-routing.md and compositions/discrete-state.md | hw-volta-participation owns ballot participation; E01 is CPU algebra, not GPU validation. |
| M07 Predicates/reconvergence as data | affordances/bit-routing.md | Exact control and primitive lowering is compiler/target-dependent; use official PTX/CUDA docs for instruction semantics and do not infer speed. |
| M08 DP4A/DP2A structural arithmetic | affordances/arithmetic-tensor.md and compositions/arithmetic-circuits.md | hw-volta-integer-routing owns exact intrinsic eligibility; hw-volta-feature-boundaries only records generation boundaries. Do not infer integer Tensor Core support on GV100. |
| M09 Packed SIMD/conversions | compositions/arithmetic-circuits.md | CUDA SIMD Intrinsics / KernelWiki doc-volta-math-12-9 is the exact source route; hw-volta-numerics owns numeric limits, while feature-boundaries covers generation only. The new Wiki page does not yet detail this family. |
| M10 SFU/interpolation alternate arithmetic | compositions/screening-refinement.md | No generic interpolator/error guarantee migrated; E26 is finite and does not bound worst case. |
| M11 FP64/wide integer paths | affordances/arithmetic-tensor.md | hw-volta-resources owns enabled product capacity; exactness remains an input/range proof. |
| M12 Register banks as operand circuit | affordances/operand-flow.md and compositions/ownership-fragments.md | hw-volta-operand-delivery records source-reported behavior, not source-level allocation; E04 is NOT_RUN. |
| M13 Operand reuse/dependency control | affordances/operand-flow.md and phase-factoring.md | hw-volta-operand-delivery; E02–E04 are scoped measurements or unrun questions. |
| M14 Register-resident local state | compositions/discrete-state.md and affordances/operand-flow.md | hw-volta-resources owns register/occupancy constraints; persistence is not cross-call storage. |
| M15 Warp/SM specialization | compositions/phase-factoring.md | hw-volta-resources/participation own resources and synchronization; no schedulability promise inferred. |
| M16 ILP/useful overlap | affordances/operand-flow.md and compositions/phase-factoring.md | hw-volta-operand-delivery; E02/E03 are selected schedules, not a general pipeline law. |
| M17 Instruction cache/phase factoring | compositions/phase-factoring.md | Volta instruction-cache facts remain source-scoped; E03/E06 do not isolate all causes. |
| M18 Shared memory as routing | compositions/ownership-fragments.md and phase-factoring.md | hw-volta-resources owns capacity/eligibility; layout-specific conflicts need measurement. |
| M19 Barriers as phase boundaries | system-boundaries.md and phase-factoring.md | hw-volta-participation owns barrier scope/visibility; E06 is selected cases only. |
| M20 L1/local memory/cold spills | affordances/operand-flow.md | hw-volta-resources owns relevant limits; spills are not automatically harmful or beneficial. |
| M21 L2 coordination service | system-boundaries.md | hw-volta-resources and source-backed evidence own capacity/behavior; no residency is inferred from capacity. |
| M22 HBM/coalescing layout | affordances/operand-flow.md and system-compositions.md | hw-volta-resources; E07 does not prove cache/TLB cause or traffic beyond its measurement. |
| M23 Constant/texture function interface | compositions/positional-routing.md and screening-refinement.md | Public texture contracts require exact primary source; E26 is a finite sample. No texture performance rule is asserted. |
| M24 Four Volta tensor microcircuits | compositions/tensor-circuits.md | hw-volta-mma plus E09 page own exact SM70 explicit PTX mapping; only this exact form is covered. |
| M25 Fragment-native intermediate | compositions/ownership-fragments.md and tensor-circuits.md | hw-volta-mma and technique-volta-fragment-layout; raw WMMA register ownership remains opaque. |
| M26 Tensor counting/reduction | compositions/tensor-circuits.md and arithmetic-circuits.md | hw-volta-mma/numerics own eligible forms; no arbitrary semiring capability is implied. |
| M27 Tensor transforms/state mixers | compositions/tensor-circuits.md | E12 page is a block-diagonal finite comparison, not a coupled recurrent transform result. |
| M28 Mixed precision/certified decisions | compositions/screening-refinement.md | hw-volta-numerics; mathematical error certificate remains workload/operator-specific. |
| M29 Atomics as merge algebra | system-compositions.md | hw-volta-participation owns supported scope/order; E14 estimated software counts, not hardware transaction counts. |
| M30 Persistent queues/interpreters | compositions/phase-factoring.md; system-boundaries.md is a secondary reachability route | hw-volta-resources/participation; E16 lost in selected cases, without proving all persistent designs lose. |
| M31 Stream memory waits/writes | system-compositions.md | hw-volta-feature-boundaries and participation for public API/order; E22 is one tested protocol. |
| M32 Cooperative grids/multidevice launch | system-compositions.md and phase-factoring.md | hw-volta-feature-boundaries owns version/admission boundary; historical APIs are not assumed available. |
| M33 Graphs/device-side launches | compositions/phase-factoring.md; system-boundaries.md is a secondary reachability route | hw-volta-feature-boundaries; E32 covers selected public routes only and does not validate restricted actors. |
| M34 Peer loads/distributed path | system-compositions.md | Pair access/order facts remain target/topology-specific; E18/E20 do not generalize across pairs or establish coherence. |
| M35 Remote atomics/NVLink signaling | system-compositions.md | hw-volta-participation and feature boundaries; peer access alone does not grant peer-atomic semantics. |
| M36 Copy engines as asynchronous workers | system-boundaries.md | Source-backed platform implementation only; public access path must be established separately. E17 unequal-work result does not prove overlap. |
| M37 Copy-engine component remap | system-boundaries.md | hw-volta-feature-boundaries; moving open-gpu-doc class source is not a public CUDA entry point. E27 NOT_RUN. |
| M38 Semaphore arithmetic outside SM | system-boundaries.md | Restricted driver/command fact only; E28 NOT_RUN and no ordinary CUDA invocation capability is established. |
| M39 QMD control object | system-boundaries.md | hw-volta-feature-boundaries; moving QMD source is a research lead. E29 NOT_RUN. |
| M40 VMM view/virtual contiguity | system-boundaries.md | hw-volta-vmm-addressing owns public mapping/access/granularity; E23 alias result is narrowly scoped. |
| M41 ATS/fault replay | system-boundaries.md | Exact ATS platform boundary stays in Atlas/source documents unless a dedicated Wiki page covers it; E24 is bounded. |
| M42 Access-counter feedback | system-boundaries.md | Driver/platform controls are not treated as a free or immediate oracle; E24/E25 remain scoped observations. |
| M43 NUMA-local host memory | system-compositions.md | Dedicated Wiki NUMA/ingress contract remains a gap; E21 node-1 bind failure means no locality comparison. |
| M44 BAR/GPUDirect/external actors | system-compositions.md | hw-volta-feature-boundaries and primary GPUDirect docs own public scope/order; addressability is not publication. |
| M45 Contexts/IPC/MPS | system-compositions.md | Versioned public compatibility facts belong in Wiki/source docs; E31 is a small client-latency sample, not fairness. |
| M46 Counters as feedback | system-boundaries.md | CUPTI/Nsight contracts belong to profiler docs; include observation overhead and replay effects. |
| M47 Special registers/local clocks | system-boundaries.md | Exact target semantics belong to primary/Wiki source; clocks are not cross-GPU time or scheduling authority. |
| M48 Cubin/SASS transformation | system-boundaries.md | hw-volta-feature-boundaries; compiler-produced binary stays the control. E30 is NOT_RUN. |
| M49 Embedded processors/firmware frontier | system-boundaries.md | No exposed programmable actor is inferred; source inspection is not an execution interface. |
| M50 Graphics/media/dormant engines | system-boundaries.md | No user-accessible CUDA route inferred from shared-die ancestry; texture design is separately bounded. |
| M51 Fault/reset/RAS | system-boundaries.md | Source-backed reliability contract remains a Wiki coverage gap; E34 is a software-visible snapshot, not a reliability claim. |
| M52 Power/thermal budgets | system-boundaries.md | hw-volta-resources and system telemetry sources; E33 is two synthetic schedules with uncalibrated telemetry. |

## Compositions C00–C39

| ID and construction | KernelBender home | KernelWiki contract/evidence or limitation |
|---|---|---|
| C00 Bit-sliced adders/Boolean rules | compositions/discrete-state.md and arithmetic-circuits.md | Mapped algebra is Bender design; E39 is not a general bitplane win. |
| C01 Two-plane sequence equality | compositions/discrete-state.md | Exact finite Boolean construction; E01 is CPU-only algebra. |
| C02 Persistent ballot-transposed state | compositions/discrete-state.md | hw-volta-participation for vote scope; include encode/decode and tail mask. |
| C03 Warp byte lookup network | compositions/positional-routing.md | Exact PRMT/shuffle forms route to hw-volta-integer-routing; participation routes to hw-volta-participation. E05 is selected cases. |
| C04 Warp CAM/group reservation | compositions/positional-routing.md | Exact match form routes to hw-volta-integer-routing; leader/participant scope from hw-volta-participation; reserve is not publication. |
| C05 A32 register graph | compositions/discrete-state.md | Bender local construction; no large irregular-graph speed claim. |
| C06 Bit-sliced finite-state engine | compositions/discrete-state.md | Keep validity mask and state encoding constraints; E01 CPU-only. |
| C07 Guard-digit convolution | compositions/arithmetic-circuits.md | Range/carry proof in Bender; exact integer instruction cost is target-specific. |
| C08 Packed integer scores | compositions/arithmetic-circuits.md | hw-volta-feature-boundaries/numerics for instructions and conversions. |
| C09 Exact bounded integers on FP64 | affordances/arithmetic-tensor.md | hw-volta-resources; proof must cover every intermediate. |
| C10 Four tiny MMA linear machines | compositions/tensor-circuits.md | hw-volta-mma and E09; exact mapping only for documented tested form. |
| C11 Tensor common-neighbor counts | compositions/arithmetic-circuits.md and tensor-circuits.md | E11 favors packed AND+POPC for one dense output at actual iteration one. |
| C12 Prefix/reduction by structured matrices | compositions/tensor-circuits.md and phase-factoring.md | E12 is only a different independent transform, not prefix proof. |
| C13 Fixed transforms as tensor circuits | compositions/tensor-circuits.md | E12 covers four independent 4-variable blocks, not a general tensor advantage. |
| C14 Certified approximate screen/refine | compositions/screening-refinement.md | hw-volta-numerics for target behavior; no Atlas error sample is a certificate. |
| C15 High/low precision composite operator | compositions/tensor-circuits.md | hw-volta-numerics; retained residual and actual arithmetic errors must be proven. |
| C16 Cancel intermediate transposes | compositions/ownership-fragments.md | hw-volta-mma/technique-volta-fragment-layout; E09 does not reveal raw WMMA slots. |
| C17 Operand-read hypergraph | affordances/operand-flow.md | hw-volta-operand-delivery is source-reported behavior, not a compiler allocation promise. |
| C18 Portfolio of pipeline work | compositions/phase-factoring.md | E03 is selected schedule contrast with unresolved cause. |
| C19 Manual Volta latency hiding | compositions/phase-factoring.md | Explicitly do not import Ampere cp.async; Wiki feature boundary identifies target split. |
| C20 Owner-compute rather than pointer chase | compositions/system-compositions.md | NVLink/topology costs remain pair/workload-specific; compare direct pull and staging. |
| C21 Support/delta rather than dense state | compositions/system-compositions.md | Representation equation is generative; protocol/base identity and reconstruction cost remain required. |
| C22 Published ring/reuse epochs | affordances/system-boundaries.md and system-compositions.md | hw-volta-participation; E15 finite protocol is not fairness or reuse proof. |
| C23 Topology-aware ownership/dual ingress | compositions/system-compositions.md | E20 pair-specific, E21 node-0 only; KernelWiki NUMA contract remains a gap. |
| C24 Monotone atomic fixed point | compositions/system-compositions.md | Must prove idempotent join, finite convergence, termination accounting, and actual atomic scope. |
| C25 Resident microservice | compositions/phase-factoring.md; affordances/system-boundaries.md is the reachability route | E16 resident path lost in selected cases; do not reject all reuse regimes. |
| C26 Copy-engine component remap | system-boundaries.md | Restricted research lead; E27 has zero executed cases. |
| C27 Command-engine completion arithmetic | system-boundaries.md | Restricted research lead; E28 has zero executed cases. |
| C28 Dependent QMD dataflow | system-boundaries.md | Restricted research lead; E29 has zero executed cases; E32 is a different public path. |
| C29 Doubled virtual ring | system-compositions.md | hw-volta-vmm-addressing and E23; same 2 MiB rounded logical domain, serial modulo baseline only. |
| C30 ATS translation-policy zoning | system-compositions.md | Platform-specific; E24/E25 do not establish general policy economics. |
| C31 Texture interpolation nonlinear element | compositions/screening-refinement.md | E26 finite errors only; no worst-case error or application crossover. |
| C32 Coarse adaptive kernel policy | system-compositions.md | E25 selected feedback result only; include observation and switching cost. |
| C33 Steady-state thermal scheduling | system-compositions.md | E33 uses two synthetic schedules and uncalibrated telemetry. |
| C34 Phase-factored circuits | compositions/phase-factoring.md | Complete-path boundary is a design hypothesis; E16/E39 do not prove a universal split. |
| C35 Positional identity deletes metadata | compositions/positional-routing.md | Treat stable local identity as representation; exact APIs and lane rules route to hw-volta-integer-routing. |
| C36 Compose lane/bank/fragment maps | compositions/ownership-fragments.md and tensor-circuits.md | hw-volta-mma, operand-delivery, and fragment-layout facts; validate full path. |
| C37 Carry-save bitset threshold | compositions/discrete-state.md and arithmetic-circuits.md | CPU algebra can test identity; GPU benefit is not established by E39's different carry chain. |
| C38 Empirical conflict maps | system-compositions.md | Observed placement hint only; no physical cache-slice/address hash is claimed. |
| C39 Representation-changing search | opportunity-index.md and phase-factoring.md | Keep formulation search small and human-selective; no optimizer or search engine added. |

## Experiments E00–E39

Every result below is indexed by KernelWiki hw-volta-atlas-evidence-index. Only
the named detailed pages make a separate evidence summary. “Source only” means
the full bounded record remains at the pinned Atlas card/evidence JSON; it is
not an assertion that the experiment did not matter. Status refers to the
campaign subset, not completion of the original protocol.

| ID | Campaign status | Migrated claim and preserved limit |
|---|---|---|
| E00 | CPU_ONLY | Inventory/capability queries only; no transfer or kernel timing. |
| E01 | CPU_ONLY | Finite host algebra/encoding checks; no GPU validation. |
| E02 | GPU_RUN | Source only; whole-kernel schedule timings do not isolate instruction latency. |
| E03 | GPU_RUN | Source only; selected schedule contrast, cause unresolved. |
| E04 | NOT_RUN | Register-bank/reuse question remains unmeasured. |
| E05 | GPU_RUN | Source only; selected warp routing/lookup cases only. |
| E06 | GPU_RUN | Source only; selected shared-bank/phase cases, no causal counter proof. |
| E07 | GPU_RUN | Source only; access-pattern timing does not establish cache/TLB cause. |
| E08 | GPU_RUN | Source only; virtual-footprint contrast, no page-placement/TLB cause. |
| E09 | GPU_RUN | hw-volta-atlas-e09-mma-coordinate; explicit PTX coordinates checked for one form, raw WMMA ownership unknown. |
| E10 | GPU_RUN | hw-volta-numerics plus index; finite numerical corpus, not an error theorem. |
| E11 | GPU_RUN | hw-volta-atlas-e11-packed-intersection; packed AND+POPC led tested dense 16x16 cases; effective iteration count one, no requested reuse sweep. |
| E12 | GPU_RUN | hw-volta-atlas-e12-independent-transform; four independent H4 blocks, not coupled M^r x. |
| E13 | GPU_RUN | Source only; selected native-arithmetic comparison with limited inputs/reuse. |
| E14 | GPU_RUN | Source only; software-estimated atomic counts, not hardware transaction counts. |
| E15 | GPU_RUN | Source only; one finite handshake, no fairness or reuse proof. |
| E16 | GPU_RUN | hw-volta-atlas-e16-resident-scheduling; resident execution slower than batching/graph replay in selected cases; no starvation proof. |
| E17 | GPU_RUN | Source only; unequal-work comparison does not establish overlap benefit. |
| E18 | GPU_RUN | Source only; one physical pair, no coherence/topology generalization. |
| E19 | GPU_RUN | Source only; full handshake timing, not primitive-only latency. |
| E20 | GPU_RUN | Source only; pair-specific payload rates, no independent link counter. |
| E21 | GPU_RUN | Source only; node-0 transfer cases; node-1 binding failed, so no NUMA comparison. |
| E22 | GPU_RUN | Source only; one tested stream-memory protocol, medians overlapped event baseline. |
| E23 | GPU_RUN | hw-volta-atlas-e23-vmm-aliasing; same 2 MiB rounded domain, one serial modulo baseline; no general ring or modulo-cause claim. |
| E24 | GPU_RUN | Source only; bounded fault/access-counter observations. |
| E25 | GPU_RUN | Source only; selected feedback comparison, no broad regret claim. |
| E26 | GPU_RUN | Source only; finite approximation cases, no worst-case error guarantee or screen/refine timing. |
| E27 | NOT_RUN | Restricted remap hypothesis; zero cases and no public-interface validation. |
| E28 | NOT_RUN | Restricted copy-engine actor; zero cases and no completion-word result. |
| E29 | NOT_RUN | Restricted QMD dependency; zero cases and no descriptor result. |
| E30 | NOT_RUN | Restricted binary transformation; zero cases and no binary-edit result. |
| E31 | GPU_RUN | Source only; small client-latency sample, not general MPS fairness. |
| E32 | GPU_RUN | Source only; selected public launch routes do not validate E28/E29. |
| E33 | GPU_RUN | Source only; two synthetic schedules, uncalibrated telemetry. |
| E34 | CPU_ONLY | Read-only software-visible RAS snapshot; no reliability claim. |
| E35 | CPU_ONLY | Software-visible inventory; no physical/electrical inference. |
| E36 | CPU_ONLY | Metadata inspection, including compiled-only cases; no runtime dispatch proof. |
| E37 | GPU_RUN | Source only; documented PTX BoolOp checks do not validate edited binaries. |
| E38 | CPU_ONLY | Five offline negative-space checks; no silicon experiment. |
| E39 | GPU_RUN | hw-volta-atlas-e39-bitplane-addition; native arithmetic generally lower for tested full paths; small bitplane median interval crossed zero, no established crossover. |

## Source registry S01–S42

S IDs below are provenance locators from Atlas sources/SOURCES.md, not KernelWiki
source IDs. KernelWiki's own source pages/IDs remain authoritative for claims
they actually cover. Unpinned or moving third-party source snapshots are not
copied into either destination.

| ID | Atlas source | Ownership / migration treatment |
|---|---|---|
| S01 | NVIDIA Volta Tuning Guide | KernelWiki doc-volta-tuning-12-9 and Volta hardware pages; source is versioned/retrieved by the Wiki. |
| S02 | V100 architecture whitepaper | Atlas source locator remains; use for platform context, not as an imported claim set. |
| S03 | PTX ISA, Atlas labels it PTX 9.4 | Do not propagate that label: KernelWiki doc-volta-ptx-8-8 records the relevant CUDA 12.9.1-era PTX 8.8 authority. |
| S04 | Jia et al. Volta microbenchmarking | KernelWiki doc-volta-jia / hw-volta-operand-delivery for bounded source-reported facts; no universal compiler rule. |
| S05 | CUDA Binary Utilities 12.9.1 | Versioned primary-source route for feature/toolchain boundaries; no binary edit capability is implied. |
| S06 | CUDA architecture support guide | KernelWiki doc-volta-toolkit-support and exact target checks; PTX/API availability differs from native support. |
| S07 | SparkAttention | KernelWiki doc-volta-sparkattention as an implementation precedent; not raw WMMA ownership authority. |
| S08 | CUDA integer intrinsics | CUDA 12.9.1 primary documentation and hw-volta-feature-boundaries for eligibility/semantics. |
| S09 | CUDA SIMD intrinsics | Same versioned CUDA primary source; preserve conversion and numeric caveats. |
| S10 | Warp-level primitives blog | Primary programming-guide route; hw-volta-participation owns exact participation contract. |
| S11 | CuAssembler upstream without pinned commit | Retained as a tooling/research lead only; not a reproducible or authorized binary-edit path. |
| S12 | VOLTA_DMA_COPY_A C3B5 class at open-gpu-doc master | Moving source locator; restricted implementation detail, never public CUDA permission. |
| S13 | VOLTA_COMPUTE_A C3C0 class at open-gpu-doc master | Moving source locator; descriptor/control fields remain research evidence. |
| S14 | NVIDIA open GPU kernel modules README | Moving upstream support locator; distinguish supported hardware from user-level invocation. |
| S15 | Volta UVM copy engine in R580.95.05 | Pinned driver implementation source; implementation behavior only, not public API contract. |
| S16 | Volta UVM MMU in R580.95.05 | Pinned driver implementation source; separate mapping/aperture behavior from CUDA VMM contract. |
| S17 | CUDA stream memory operations 12.9.1 | Public API facts go to feature-boundary/participation pages; E22 is workload-specific. |
| S18 | CUDA low-level VMM introduction | Conceptual background only; exact operation/granularity/access comes from S31 and hw-volta-vmm-addressing. |
| S19 | Tensor-core reduction/scan paper | Design precedent for Bender constructions, not a Volta performance guarantee. |
| S20 | FTTN numerical testing | KernelWiki doc-volta-fttn; methodology/findings stay bounded to reported corpus. |
| S21 | Tensor Core programmability/performance/precision paper | Numerical design background; does not guarantee the same accuracy or performance for another operator. |
| S22 | CUTLASS v2.11 SM70 MMA source | Version-pinned implementation reference; PTX interface authority remains NVIDIA PTX docs. |
| S23 | CUTLASS v2.11 Volta multiplicand layouts | Version-pinned example connected to technique-volta-fragment-layout; not an intrinsic storage contract. |
| S24 | tcFFT paper | Research precedent for fragment manipulation; no general tensor-fragment speed claim. |
| S25 | NVSHMEM latest documentation | Moving/version-sensitive public API locator; no unpinned behavior copied as a stable contract. |
| S26 | NCCL 2.18.6-1 LL128 source | Pinned implementation precedent; not a guarantee for another transport or API. |
| S27 | Volta QMD at open-gpu-doc master | Moving restricted descriptor source; E29 is NOT_RUN and no user entry point is inferred. |
| S28 | Volta UVM fault buffer in R580.95.05 | Pinned driver source; bounded implementation evidence only. |
| S29 | UVM access counters in R580.95.05 | Pinned driver source; policy feedback is delayed/batched and platform-specific. |
| S30 | CUDA C++ Programming Guide 12.9.1 | Primary public API/source route; apply exact version/target support. |
| S31 | CUDA VMM Driver API 12.9.1 | hw-volta-vmm-addressing owns public reserve/map/access/granularity details. |
| S32 | CUDA Device API 12.9.1 | Public device/capability queries; eligibility must be queried/qualified for exact target. |
| S33 | GPUDirect RDMA 12.9.1 | Public registration/BAR/order facts belong to exact API source; addressability alone is not synchronization. |
| S34 | CUPTI current documentation | Profiling source; current version must be checked, and measurement overhead belongs in cost. |
| S35 | Nsight Compute current guide | Profiler mechanics remain with ncu-report-skill/primary guide, not KernelBender. |
| S36 | nvidia-smi current documentation | Current topology/power/reset telemetry locator; values are host/product-specific. |
| S37 | Nouveau GV100 graphics at Linux v6.12 | Pinned open-driver implementation; not evidence of a CUDA-accessible graphics engine. |
| S38 | Nouveau GV100 MMU at Linux v6.12 | Pinned implementation source; do not generalize to the NVIDIA proprietary driver contract. |
| S39 | Nouveau GV100 ACR at Linux v6.12 | Pinned authenticated-code implementation; firmware-level research lead only. |
| S40 | Nouveau GV100 FIFO at Linux v6.12 | Pinned scheduling/queue implementation; not an application submission API. |
| S41 | NVIDIA MPS latest documentation | Version-sensitive compatibility source; E31 remains a bounded client-latency sample. |
| S42 | CUDA Driver API types 12.9.1 | Public enum/capability definitions; exact behavior stays with the selected operation page. |

## Navigation and evidence framework

The standalone START_HERE.md, NEED_INDEX.md, and FIELD_GUIDE.md are not copied
as documents. Their problem-first route, evidence axes, and design methodology
are synthesized into KernelBender's opportunity index, ten bridges, design
brief, experiment guidance, and source map. The Atlas reader/manifest is not
ported as infrastructure: authored Markdown links and small targeted reads are
the active retrieval mechanism. KernelWiki's schema/query system remains the
only hardware/evidence database.
