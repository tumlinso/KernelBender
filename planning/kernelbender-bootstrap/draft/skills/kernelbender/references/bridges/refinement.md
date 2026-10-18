# 09 — Spend exact work only where uncertainty requires it


**Recognition cue.** The caller needs a decision or screened subset, most cases are far from a boundary, and a cheaper approximation with a justified error envelope exists.

**Construction.** For required predicate `s >= tau` and a valid bound `abs(s-shat) <= epsilon`, accept when `shat-epsilon >= tau`, reject when `shat+epsilon < tau`, and refine otherwise. The output decision remains exact relative to the defined s only if the bound includes the real input conversion, arithmetic, interpolation and extraction errors. A mask can route ambiguous cases without materializing all scores.

An alternate form is a bounded smooth function tabulated for a supported texture/interpolation path. Ideal linear interpolation error `h^2*max(abs(f''))/8` is only one component; table quantization, coordinate/filter precision and exceptional regions also count. A polynomial or SFU seed+refinement may be cheaper and easier to bound.

**First discriminator.** Establish the bound or explicitly classify the path as approximate under caller permission. Measure ambiguity rate and the entire fast+refine route against direct evaluation and a simpler filter. Include queue/compaction cost and near-threshold inputs. Finite random agreement does not certify exact decisions.

**Failure boundary.** When most cases are ambiguous, bookkeeping can add cost without reducing exact work. A looser output tolerance is a different task unless authorized. Do not create hidden numerical slack to turn a design into a win.

Sources: [AT-C14], [AT-C31], [AT-R15]. These are source-backed constructions and hypotheses, not locally measured KernelBender speedups.
