# Operand flow, local state and phase boundaries

The value that reaches an instruction is a sequence of loads, register reads, exchanges, dependencies and live ranges. This affordance family changes that path while keeping useful arithmetic fixed. Its ideas are particularly target-sensitive: retrieved exact facts from `hw-volta-operand-delivery`, `hw-volta-resources`, `hw-volta-mma` and `hw-volta-participation` before turning a diagram into CUDA.

## Retain the representation where its next consumer can use it

Write a semantic coordinate's producer ownership `P(x)=(lane,slot)` and consumer ownership `Q(x)=(lane,slot)`. A conversion is the map from `P` to `Q`. If an intermediate canonical store and a following retile are inverse operations, remove both and make the middle operator consume the retained layout. For an elementwise `f` and permutation `p`, `p(f(x))=f(p(x))` when parameters follow the same permutation. For a reduction, additionally prove that the reduced coordinates and participants are correct.

This can compose fragment outputs with masks, normalization factors, a following matrix product or another local stage. The explicit map must identify each scalar, lane and slot; equal matrix shapes do not guarantee direct accumulator/operand compatibility. Retained distributed state can save conversions yet add shuffles, barriers, live registers, or spills. Compare the whole producer-consumer chain and keep a materialized/library boundary as a serious alternative. (Atlas M18, M24, M25; C16, C36.)

## Choose the operand graph, not a magic register number

For a hot instruction window, list each distinct input and which operations consume it. This graph suggests candidate schedules: reuse an operand near its consumers; place independent required work between dependent operations; or make an amortized copy if it shortens a repeated-delivery bottleneck. The schedule must preserve data dependence and actual useful work. Register banking, compiler assignment and stall metadata are implementation facts, not universal source-level guarantees. A local bank fix can increase live ranges or harm another instruction.

Treat shared memory as a second routing and ownership fabric. A producer's swizzled/banked map may make an exchange or tensor operand load direct. Follow it through the consumer: bank conflicts, address arithmetic and synchronization can simply move to the next phase. Compare the actual exchange with a warp shuffle, direct coalesced load and a library tile. Keep facts about shared capacity, bank behavior and legal barriers in exact-target pages. (Atlas M12, M13, M18, M19; C16, C17, C36.)

## Hold a small state only within a justified lifetime

Per-thread registers can hold a small local graph, FSM or coefficient state through several transitions. A small, statically indexed state may eliminate reloads and expose the rule as a circuit. It costs registers and potentially duplicated state. Dynamic local arrays can become memory-backed; ordinary kernel completion destroys register state. A cross-call cache needs a real allocation, update/invalidation contract, capacity budget and concurrency ownership.

Use the full region cost:

```text
cost(r) = prepare(r) + uses * per_use(r) + updates * maintenance(r) + extraction(r)
```

Include synchronized staging, allocation and required output where the caller pays them. If a recurring path loses, increasing reuse alone does not rescue it. Capacity reduction and throughput are separate outcomes. For low-bit or compact input, compare decode-once plus a strong library, decode into consumer ownership, and direct fused computation while keeping the decoded numerical operator identical. (Atlas M14, M20; C02, C05, C06.)

## Parallel schedule is part of the representation

Independent tasks may be split across multiple partial results if an associative or otherwise valid merge exists. For a known affine segment, `(A1,b1)` followed by `(A2,b2)` composes as `(A2*A1, A2*b1+b2)`. This may expose parallel prefix structure, but the summary can be more expensive than the original update. A device-resident queue or specialized loader may retain useful data, but requires bounded producer/consumer progress and enough resident resources. Test ordinary batching and graph replay first; the Atlas's selected persistent comparison lost to both. (Atlas M15–M17, M19; C18, C19, C25, C34.)

Big fused circuits also have a code and live-state working set. Factor a frequent hot phase from rare or bulky paths when that reduces instruction footprint or exposes more independent tasks. The new boundary adds stores, reloads, dispatch and synchronization. Repeated phases can be reusable functions without assuming a persistent execution service. A smaller binary is not automatically faster; require evidence that instruction delivery, live state or scheduling limits the old path.

## Cost test and falsifier

Compare (1) the strongest materialized or library chain, (2) retained producer/consumer ownership and (3) a phase-factored option only if there is a concrete issue it addresses. Hold arithmetic, input and output semantics constant. First validate labeled ownership, state updates, all participants and the merge equation. Reject a candidate if it creates cross-warp movement where none existed, spills, uses a nonprogressing spin wait, extends too many live values, or saves no conversion that the caller actually pays.

**Bounded evidence:** E09 establishes one explicit PTX ownership mapping but leaves WMMA raw slots open. E16 found the measured resident path slower than batching and graph replay at its tested task counts; it does not reject all state reuse or role specialization. Exact source/measure scope is in [KernelWiki contracts](../wiki-contracts.md), especially `hw-volta-operand-delivery`, `hw-volta-participation` and `hw-volta-atlas-e16-resident-scheduling`.

Atlas IDs: M12–M20, M24–M25; C02, C05–C06, C16–C19, C25, C34, C36; E04, E06, E09, E16, E30, E32. Source checkout: [ATLAS5B5629B](../sources.md#atlas-identity).
