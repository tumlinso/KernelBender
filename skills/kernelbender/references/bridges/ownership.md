# 03 — Compose layouts instead of repeatedly canonicalizing


**Recognition cue.** A producer writes canonical memory solely because the next operation expects a different layout. There is no external requirement for that intermediate arrangement.

**Construction.** Write ownership of semantic coordinate x as `P(x)=(lane,slot)` in the producer and `Q(x)=(lane,slot)` in the consumer. The move is the mapping from P to Q, not an ordinary shape reshape. Compose a producer's canonicalization with the consumer's retile; inverse steps may disappear. For an elementwise function f and permutation p, `p(f(x))=f(p(x))` when the associated parameters follow the same permutation. A reduction can remain in a distributed representation only if its axes and collective participation remain correct.

Choose the end-to-end global/shared/register path jointly. Sometimes a replicated constant or a different consumer tile costs less than general exchange. Sometimes canonical materialization is the right boundary because it shortens live ranges or lets a better library compute the next stage.

**Hardware boundary.** Use the exact documented fragment form. SM70 explicit PTX maps do not license arbitrary WMMA raw storage. All required lanes execute a collective. Matching matrix dimensions does not establish accumulator-to-operand compatibility. [AT-R05, AT-E09]

**First discriminator.** Validate a labeled/one-hot ownership map, then compare the complete producer+consumer with arithmetic held fixed. Count shuffles, shared exchanges, conversions, barriers and spills. A lower move count can still create a longer dependency chain. FP16 versus FP32 accumulation is a different numerical experiment, not a layout-only win.

Sources: [AT-C16], [AT-C36], [AT-M25].
