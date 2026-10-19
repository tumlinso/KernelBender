# Composition: move only the information the owner cannot keep local

**Use when:** data is partitioned across GPUs, host memory, or virtual views, and the communication or address boundary is large relative to useful work. The representation change is to move a query, support/delta, or compact answer rather than always moving a dense payload. Public reachability and ordering must be established independently from the idea.

## Owner-compute versus pull and stage

Suppose a requester needs `g(x)` for remote owner-held state `x`. Compare semantically equivalent paths:

```text
pull  = request + remote bytes / directed_rate + requester g(x)
stage = copy/setup + full bytes / directed_rate + local reuse of x
owner = owner_queue + owner g(x) + compact reply / directed_rate
```

If only a predicate, count or support mask is needed, `g` at the owner can return much less information than `x`. If the requester needs dense values once, direct pull or bulk stage may be simpler; if it reuses many owner values, staging may amortize; if its query is compact and the owner already has a useful local layout, owner-compute may reduce traffic. Include request latency, queueing, endpoint contention, synchronization, reply handling and tails. A remote pointer by itself gives neither a protocol nor free memory. (Atlas M34–M35; C20, C23.)

For candidate partition `p`, account for local compute and exchanged data as `T_p = local_work_p + messages_p*startup + bytes_p/effective_rate + synchronization_p`. Compare the same operation under owner-compute, requester-pull, batched staging, and if suitable, an established communication collective. Topology-aware placement is a workload fact to query and measure; a historical pair's link rate is not a universal capacity. Host NUMA placement, pinned/page-locked memory and GPU direct ingress each have distinct source and lifetime contracts. (Atlas M43–M45; C23.)

When shaping a partition, compare useful values with actual transferred sectors and owner-side memory work. A layout chosen only for logical edge count can create poor transactions or move cold metadata with hot payload. Measure the real allocation and access pattern, then treat an inferred placement map as a tuning hint rather than a correctness invariant. KernelWiki's `hw-volta-resources` holds target facts; Atlas E07/E20 do not establish a general cache- or NVLink-cause model. (Atlas M22; C23, C38.)

## Send a delta only against a known base

If receiver state has `n` values of width `w`, a delta with `k` changed entries and index width `i` has a first-order payload of `k(i+w)` bytes versus dense `nw`. The delta is potentially smaller when `k(i+w)+header < nw`; discovery, encoding, base retention, epoch validation, decode and dense fallback also cost. It is useful when the receiver can apply the delta to the exact identified base and downstream consumers can stay in the updated representation. A stale epoch, different base or frequent near-dense updates invalidate the savings. (Atlas M06; C21.)

The exact design may transmit a bit support mask rather than explicit indices when the universe is small and stable. If the receiver only needs to know whether any update exists, a reduction/summary can be enough. Compare these payloads with the existing dense path and current communication library on the actual directed topology. The encoding must preserve ordering, duplicate, overwrite and numerical semantics.

An update may also be combined before it crosses a boundary when its algebra supports that combination. If `x ← x ⊔ d` is associative, commutative and idempotent over a finite-height state space, duplicate proposals can merge without depending on arrival order; reachability bitsets with join `OR` are one example. Termination still depends on a scheduler that eventually processes all pending and in-flight updates. Compare with a conventional frontier plus aggregation and count duplicate work, hot-target contention, queue state and termination checks. Floating addition and overwrite do not inherit this property. (Atlas M21, M29; C24.)

## Make a periodic view without duplicating payload

For a ring of `N` elements, a virtual interval of length `2N` can in principle map the same backing allocation into adjacent halves. A window of length at most `N` then has a single contiguous address range from a start in the first half. The algebra eliminates the wrap split; it does not establish visibility between aliases, permission, granularity or cheaper translation. Compare with modulo indexing, power-of-two masking when valid, and a two-segment window.

The full economics are `mapping setup / uses + view walk + translation and cache behavior` against the complete conventional walk. Count allocation granularity, alignment, setup, address arithmetic, actual access shape, cache and remapping phase boundaries. Keep ordinary CUDA VMM as a candidate only when KernelWiki's `hw-volta-vmm-addressing` supports the target/runtime use. Never use direct page-table or PTE edits as if they were a public view API. (Atlas M40–M42; C29, C30.)

Atlas E23 compared two fixed aliases with one serial modulo ring traversal and found lower device-walk medians in the tested cases. Both requests (4,096 and 65,536 elements) rounded to the same 2 MiB mapping granularity and 524,288-element logical domain. There was no power-of-two-mask or optimized two-segment comparison, so the result does not isolate modulo or establish general VMM benefit. Query `hw-volta-atlas-e23-vmm-aliasing` for that bounded evidence.

## Access, correctness and experiment

A small resident palette can retain fixed coefficients and compact task state, but it reserves execution resources and needs a queue/drain protocol. Compare with finite batching and graph replay before assigning a worker role. If the dependency graph is known and finite, a captured graph can amortize host submission while retaining ordinary kernel boundaries. Cooperative-grid admission and public stream-memory operations have their own exact API, target, scope and progress contracts; compare with multi-kernel/event boundaries and avoid assuming an oversubscribed grid will progress like a global barrier. For Volta, retrieve `hw-volta-participation` and `hw-volta-feature-boundaries`. Atlas E16 found resident execution slower than batching and graph replay in its tested cases; E22's stream-memory medians overlapped its event baseline; E32's selected graph/launch comparison does not validate restricted command paths. (Atlas M30–M33.)

Check exact target, public interface, lifetime, mapping permissions, owner identity, participant scope, ordering and progress using the [KernelWiki contract map](../wiki-contracts.md). A source-reported remap, QMD dependency, command-engine semaphore or firmware feature can remain a useful research direction, but it is not an ordinary kernel construction until an owned supported invocation path is demonstrated. Preserve a public kernel/copy/graph baseline and do not rely on unavailable capabilities.

First validate the logical answer and communication protocol under delayed, empty, duplicate, stale and wraparound cases. Measure the full caller-visible operation including copy/setup, producer/consumer synchronization, compact response handling, updates and multiple uses. Reproduce on the actual device pair/host topology. Reject the transformation if it merely changes where work occurs, fails to make progress, depends on unsupported access, or saves bytes that the consumer immediately reconstructs.

For the other compositions in this family—including bounded queue epochs, monotone fixed points, resident palettes, copy-engine roles and restricted command experiments—open [system boundary affordances](../affordances/system-boundaries.md). That card keeps confidence, access and evidence separate and preserves NOT_RUN restrictions.

Atlas IDs: M06, M21–M22, M29–M45; C20–C24, C29–C30; E07, E16, E18–E24, E32. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
