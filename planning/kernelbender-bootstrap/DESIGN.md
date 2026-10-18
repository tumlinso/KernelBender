# Decision: a representation-and-lifetime design skill

## 1. The refined problem

The design opportunity is not that an agent lacks CUDA advice. The existing CUDA skill already asks it to begin from a semantic unit, choose representations and ownership, compare unlike candidates, price reuse and test falsifiers. The Atlas already has a representation-changing search procedure. A new instruction saying “be creative” or “step back” would duplicate that work. [CUDA-MAD, AT-C39]

The gap worth targeting is **turning a specialized application's structure into a concrete, architecture-realizable computational design before familiar operator boundaries become fixed**. KernelBender should improve the probability of finding a useful formulation that normal recipe retrieval or local tuning would miss. Examples include keeping categorical state as bitplanes across several transitions, returning a threshold mask without constructing scalar counts, folding immutable linear consumers into preparation, or composing producer/consumer ownership rather than canonicalizing every intermediate.

The central question is:

> Given the caller's required observable behavior, legitimate invariants, update and reuse pattern, and target hardware, which representation and execution structure makes the whole permitted computation cheapest—and what would distinguish that design from its strongest alternative?

“Cheapest” is task-owned: latency, throughput, capacity, energy or an explicit combination. The skill does not select the objective. A capacity-saving representation may be useful without a speed win, but cannot be sold as a throughput improvement.

## 2. The caller is an engineering agent, not a blank model

A KDA agent typically has a task contract, local source and independent evaluation path. Sometimes it has a measured incumbent; sometimes it is designing a new fused operation. It needs a **decision-bearing design brief**, not a lecture or another plan authority. KDA already owns candidate snapshots, trusted inputs, evaluation rounds, selection and evidence. KernelBender should feed that machinery better candidate hypotheses and constructions. [KDA-ENGINE, KDA-FLOW, KDA-CLI]

KernelBender can be useful at three points: before the first implementation of a specialized operation; after evidence exposes a structural bottleneck; or when successive changes remain in the same design family without progress. It should not become compulsory on every build, ordinary GEMM request or known synchronization repair. Explicit requests to reconsider the formulation remain valid even when a conventional path is strong.

Its value does not depend on there already being a slow kernel to profile. Profiling describes an implementation; a new formulation can instead start from equations, interface constraints, a source-backed capability and a cost hypothesis. These are hypotheses, not measured bottlenecks. For an existing hotspot, consume ncu-report-skill's diagnosis rather than bypassing it. [NCU-SKILL, NCU-VOLTA]

## 3. Chosen intervention

The proposed method is a flexible **reframe–connect–construct–discriminate** loop, not a fixed brainstorming ritual.

**Reframe.** Separate required behavior from inherited implementation conventions. Follow the requested outputs backward and the input/state lifecycle forward. Which outputs/intermediates are externally visible? Which quantities are fixed per build, update epoch, batch or call? What must remain exact, and which rounding/ordering changes are permitted? How often does a prepared representation really survive unchanged?

**Connect.** Retrieve a few mechanisms by the algebra and information movement required, not only by operator names. Each mechanism bridge supplies a recognition cue, concrete mapping, capability boundary, economic opportunity, a failure case and a discriminating test. The agent may also propose an unlisted mechanism, but must establish its actual computational and hardware contract rather than invent an instruction.

**Construct.** Describe a materially different representation or execution structure: where semantic values live, who produces/consumes them, what work disappears and what new work appears. Usually retain the strongest conventional route and one or two genuinely unlike alternatives. There is no minimum candidate count, no novelty quota, and no rule requiring a Tensor Core or other exotic unit.

**Discriminate.** Choose the smallest experiment or missing fact that changes the decision. A valid experimental design can be speculative; a claimed hardware guarantee cannot. Distinguish a test of feasibility, of causal mechanism and of full-path benefit. For an optimization claim, keep semantics fixed and include the costs the caller actually pays.

These moves can interleave. An unexpected counter result can change the representation; a semantic argument can eliminate a candidate without compilation. KernelBender should finish with a next engineering action, not an indefinite request for further analysis.

## 4. The organizing unit: a complete economic region

A kernel boundary is an implementation choice. The relevant region ends where the caller observes, updates, invalidates or must reconstruct a representation. It may span several launches or repeated calls; it may also be a single small operator when the interface fixes everything else.

For representation r over n uses and u updates, a useful first model is:

`C(r) = preparation(r) + n * per_use(r) + u * maintenance(r) + extraction(r)`

Include workspace, transfers, synchronization and resource interference in the appropriate terms. A pipeline term is a critical-path/shared-resource cost, not necessarily the sum of independently measured components. “Zero-copy” and “resident” do not set these terms to zero. [AT-R11, AT-R14]

If delta is a positive measured or plausibly bounded per-use saving, additional preparation P and maintenance U repay only when `n*delta > P+U`. If delta is nonpositive, increasing reuse alone does not rescue that particular implementation. This says nothing universal about other mappings of the representation. The W4A16 measurements are a concrete warning: one direct SIMT decoder losing to predecode+cuBLAS does not prove every consumer-native decode path is inferior. [KW-LOWBIT]

There is also a physical lifetime boundary: register contents do not persist across completed kernel launches. Cross-call reuse needs an actual retained allocation, recomputation strategy or authorized persistent execution. Mathematical equivalence does not provide a storage lifetime.

## 5. The knowledge contribution

The initial skill contains ten compact mechanism bridges, organized by what they can eliminate or make native:

1. Compute the demanded result instead of conventional intermediates.
2. Move invariant work to preparation and maintain a useful representation.
3. Compose ownership maps across stages.
4. Use packed Boolean state and carry-save threshold logic.
5. Make stable position carry identity and local topology.
6. Express an operation in an alternative arithmetic resource.
7. Factor dependency through a mergeable summary.
8. Expose useful parallelism and choose phase boundaries jointly.
9. Use approximation only within the real decision/error contract.
10. Reduce information crossing a boundary or change a permitted view.

These are not replacements for all Atlas cards. They add a **problem-to-mechanism bridge** and a construction example, with direct source locators. The Atlas's speculative, reverse-engineered and public-API categories remain distinct. A broad concept may transfer between GPUs while its instruction form, participant scope and cost do not. [AT-START, AT-NEED, AT-R05, AT-R06]

The full research dossier should not load into every invocation. A short SKILL entry and need map select just enough material to make a design decision. Progressive disclosure is supported by the skill format; its effectiveness here is an evaluation question, not a proven token-budget optimum. [SKILLS-SPEC, OPENAI-SKILLS]

## 6. Why this is the best-supported initial choice

| Alternative | Useful aspect | Why not choose it as the primary design |
|---|---|---|
| A short creativity/step-back prompt | Low overhead; useful abstraction cue | Existing CUDA/Atlas guidance already does this; risks no added capability |
| A complete Atlas port | Rich unusual substrate | Too much context, duplicate authority, no proof the old organization serves the new caller |
| A profiler-first optimizer | Evidence-driven revisions | Duplicates ncu/KDA and cannot frame a computation that has not been implemented |
| Fixed three-way brainstorming or mandatory lenses | Encourages alternatives | Ritual work and shallow variants; can suppress a simpler correct decision |
| Multi-agent tournament or evolutionary search | More exploration | New orchestration, budget and evaluation complexity before proving the knowledge intervention |
| Symbolic superoptimizer/e-graph implementation | Joint algebra/schedule search | Different product; requires an IR, numerical semantics and backend ownership. Learn from Mirage/Prism, do not reimplement them |
| A giant capability registry/automatic retrieval service | Machine-readable routing | Premature given a small corpus and capable semantic caller |
| **Selective design guidance plus mechanism bridges** | Concrete substrate, broad problem framing, direct handoff | Chosen; incremental effectiveness must be established against the existing competent baseline |

The initial choice is not a claim of global optimality. Its advantage is that it attacks the identified gap directly, composes with the integrated system, and permits a cheap falsification: compare it with the current method under matched budgets.

## 7. Creativity and correctness are not opposing goals

The skill should broaden permissible formulation choices, not relax the user contract. Exploit invariants supplied by the application, statically established properties or runtime guards with a valid fallback. Do not treat sampled input distributions, fixed RNG seeds, missing oracle cases or repeated benchmark buffers as semantic guarantees.

For novel arithmetic, distinguish real-number identities from the requested finite-precision computation. For concurrency, separate participation, visibility and progress. For new mechanisms, distinguish source support, target applicability, public reachability and local qualification. Correctness requirements constrain the design space but do not compel conventional designs. [AT-R06, AT-R15, KDA-STUDY]

Conversely, do not demand full proof of profitability before proposing a candidate. The purpose of an experiment is to resolve uncertainty. Reject obvious illegality and well-supported domination; retain an uncertain but discriminating option when testing it could reveal a better family. Never optimize a surrogate such as occupancy, peak instruction rate or minimum byte count instead of the caller's objective.

## 8. What completion means

Deliver a compact, installable skill with usable bridges, evidence-preserving examples, natural KDA integration and a bounded evaluation. The final report must distinguish three outcomes: the files and integration work; the skill changes design behavior in useful ways; the resulting kernels improve on equal-budget controls. These are separate claims.

A package that validates structurally is not evidence of creativity. A good KDA attention result produced before KernelBender exists is an illustrative case, not a KernelBender success. A pilot that finds no incremental benefit is legitimate evidence to simplify or restrict the skill rather than expand its machinery. The implementation plan makes that assessment explicit.
