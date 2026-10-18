# 04 — Treat scalar logic as parallel Boolean circuits


**Recognition cue.** Many independent discrete states share one rule, or many masks need a per-position count/threshold. Ordinary tensors are not the only useful representation.

**Substrate.** A machine word can hold one bit for many independent instances. With bitplanes a,b,c, define `s=a XOR b XOR c` and `k=(a AND b) OR (a AND c) OR (b AND c)`. At each bit position `a+b+c=s+2k`. The carry remains a separate plane: no integer carry is allowed to leak between unrelated positions.

**Construction.** Combine equal-weight planes in a carry-save tree, then compare the weighted planes with a threshold directly. For a simpler three-mask majority, k itself is the requested output. This is not `popcount(a)+popcount(b)+popcount(c)`, which answers an aggregate question. For a finite-state rule, derive the Boolean outputs from the actual truth table and reuse subexpressions across state planes. Retain the encoding when later consumers can use it.

**Hardware boundary.** Compiler-generated logic may already select efficient instructions; hand-written PTX is not automatically better. Native logic/ballot/shuffle forms and partial-lane masks must be checked for the target. Cross-word neighbors and differing rules per instance require explicit routing/selection.

**First discriminator.** Exhaust small truth tables and tail masks on CPU, then compare a strong packed-bit baseline and scalar/tensor alternative including both transposes and extraction. Aggregate-only counts may favor simple POPC; ordinary scalar additions may favor native arithmetic. The Atlas E39 full-adder result is a counterexample to automatic bit-slicing wins, not a disproof of categorical/threshold designs.

Sources: [AT-C00], [AT-C37], [AT-M06], [AT-E39], [PTX].
