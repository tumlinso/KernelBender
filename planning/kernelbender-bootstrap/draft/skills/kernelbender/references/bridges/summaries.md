# 07 — Replace apparent sequence with a composable summary


**Recognition cue.** A reduction or state evolution appears sequential, but a bounded summary of a segment might compose with another summary.

**Construction.** For an affine state update `x' = A x + b`, two known segments compose chronologically as `(A2,b2) after (A1,b1) = (A2*A1, A2*b1+b2)`. This can expose parallel prefix/segment work. It is useful only if summary construction/composition is cheaper than the original sequence at the required dimension and all needed inputs are actually available.

Online normalized reductions are another case. A softmax block can retain maximum, shifted exponential sum and weighted numerator `(m,l,u)` rather than a full probability tensor. Stable merging rescales the two summaries to their joint maximum. Empty/masked segments need explicit handling; the state must include all information the consumer requires.

**Failure boundaries.** A nonlinear or data-dependent recurrence does not become affine by naming a matrix. A compact-looking state can require a dense expensive summary. Reassociation changes floating evaluation and needs the caller's numerical permission. Decode cannot use future input tokens that do not exist yet.

**First discriminator.** Compare direct sequential work, useful batching and one summary/chunk candidate including preparation and final merge. Test segmentation invariance, initial/final state and adversarial ordering under the stated tolerance. A caller requiring every intermediate state may change the output and storage cost.

Sources: [AT-R11], [AT-R15], [KW-RECURRENCE], [KDA-STUDY], [FLASH]. The affine identity is a mathematical construction, not proof of a faster GPU scan.
