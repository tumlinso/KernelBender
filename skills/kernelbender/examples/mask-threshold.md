# Example: counts are only an intermediate

**Status:** exact Boolean identity; GPU mapping and benefit unmeasured.

A caller supplies many bit masks over the same local population and asks which positions occur in at least t masks. It does not need scalar counts or one total population count.

A conventional path expands each bit into counters, sums and thresholds. An alternative keeps per-position counts in weighted bitplanes. Three equal-weight planes a,b,c reduce to `s=a XOR b XOR c` and `k=majority(a,b,c)`, with `a+b+c=s+2k` independently at every bit. Repeating that reduction yields a compact weighted representation; compare it to t directly rather than decode every count.

For three masks and t=2 the majority plane is already the result. For larger input counts, carry-save construction and a bitplane comparison are required. The algorithm must not shift carry into a neighboring bit position or confuse aggregate POPC with per-position multiplicity.

The economic region depends on the caller. If masks already arrive packed and the next stage consumes the result mask, both expensive representation boundaries may disappear. If the caller supplies scalar categories and needs all scalar counts on every step, those conversions can reverse the choice. A good test includes both legitimate contexts and uses an efficient packed baseline.

Small exhaustive truth tables and tail masks validate the identity. Native benchmarks then decide whether this particular mapping beats conventional alternatives. The Atlas's ordinary full-adder experiment is a counterexample to blindly applying bitplanes, not a result about this different threshold operator. Sources: [AT-C00], [AT-C37], [AT-E39].
