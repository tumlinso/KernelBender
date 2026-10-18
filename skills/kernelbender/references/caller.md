# Recover the actual design freedom

The best representation depends on what the caller requires across a lifetime, not only on a tensor shape. Read the existing contract and source; do not make the caller fill a new form when the information is already available.

| Question | Why it changes the design |
|---|---|
| Is the output a whole tensor, a few projections, top-k IDs, a threshold mask, or updated state? | Computing unused intermediates may be avoidable. |
| Must intermediate values be externally visible or rounded in a prescribed format? | Reassociation/fusion may otherwise change the specified function. |
| Which coefficients, topology, layouts or supports remain unchanged, and until when? | Preparation can move to an update boundary only with valid invalidation. |
| Which guarantees are structural, supplied, proved or guarded? | Observed distributions and convenient fixtures are not permissions to specialize. |
| Can internal representation persist between stages/calls? | Retaining state needs a real lifetime and memory owner. |
| Is the objective per-call latency, steady throughput, total epoch cost, capacity or another quantity? | Setup exclusion and reuse can reverse the answer. |
| Are code size, workspace, launch count, latency tails or dependency choices constrained? | A globally faster average may still violate the caller's needs. |
| What target/API/toolchain and experimental access are actually available? | A name such as “Volta” or “Tensor Core” is not an exact implementation contract. |

A compact lifecycle sketch is often enough:

`external input → preparation/update → retained representation → repeated consumers → required output/invalidation`

Annotate each arrow with movement/conversion, owner and frequency. Mark whether it is required by the application or inherited from a library boundary. Include aliases and overlapping/concurrent uses where they affect correctness.

No measured incumbent is required to frame a new design. Use a simple reference or strong library route for the first comparison. If a target or key semantic condition is unknown, keep it unknown and give conditional designs or request the single missing fact that blocks a consequential choice. Do not infer available future recurrent inputs, hidden sparsity, relaxed precision or immutable weights.

A source identity plus a proved map can support a mathematical construction. It does not establish register residency, native instruction selection or end-to-end benefit. Those become targeted implementation tests, not prose assertions.

Sources: [CUDA-MAD], [AT-R11], [AT-R15], [KDA-ENGINE].
