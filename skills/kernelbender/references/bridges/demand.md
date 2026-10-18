# 01 — Compute only the information the consumer requires


**Recognition cue.** The conventional pipeline builds a large result but the caller only needs a projection, mask, statistic or final state. The representation may contain more information than the observable requires.

**Construction.** Let a fixed matrix W and fixed consumer V define `Y=(XW)V`. If no intermediate XW is observable and the contract permits the changed floating evaluation, prepare `C=WV` once and compute `Y=XC` for each X. The output dimension of V, update frequency and preparation cost determine whether this is useful. Another case is returning a per-position threshold mask directly from count bitplanes rather than decoding every count.

This is not simply fusing kernels: it can remove an entire intermediate computation. Work backward from the demanded output and ask whether a sufficient representation or algebraic factor exists. A nonlinear consumer, required intermediate rounding, changing parameters or externally visible intermediate can invalidate the substitution.

**Economic question.** Compare preparation plus repeated use and invalidation with the best unchanged library chain. Include the new representation's footprint. Do not precompute per-input answers or exploit fixed evaluation inputs.

**First discriminator.** Test operator equivalence under the actual numerical policy before timing. For a real-algebra identity, compare both evaluation orders to the independent oracle and verify permitted error; for strict staged rounding, retain an order-preserving path. Sweep only the update/reuse cases that could reverse the decision.

**Transfer.** Small statistics of large intermediates occur beyond ML. The relevant property is the consumer's information demand, not a kernel name. Sources: [CUDA-MAD], [AT-C35], [MIRAGE], [FLASH]. This is a derived design example, not a measured KernelBender result.
