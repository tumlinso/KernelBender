# E02 — Preserve every position through a local state transition

A periodic one-dimensional array has one two-bit state and one mask bit per
site. For each synchronous step, site `i` reads its old state `s[i]`, the old
state of its left neighbor `s[(i-1) mod N]`, and `mask[i]`, then writes
`rule[s[i]][s[(i-1) mod N]][mask[i]]`. The complete final state at every
position and the count of final states equal to `3` are required. No
intermediate step is externally visible. The rule and mask are fixed during
one epoch and may change before the next. Use `N=31`, `33`, `1024`, or `65537`
and `T=1`, `8`, or `32` steps. State, mask, and output are byte-per-site at
the API boundary. The 32-entry rule table is:

```text
state 0, left 0..3, mask 0 then 1:  0, 1, 2, 3, 0, 1, 2, 3
state 1, left 0..3, mask 0 then 1:  1, 0, 3, 2, 3, 2, 1, 0
state 2, left 0..3, mask 0 then 1:  2, 3, 0, 1, 2, 3, 0, 1
state 3, left 0..3, mask 0 then 1:  3, 2, 1, 0, 1, 0, 3, 2
```

Compare a conventional implementation with any genuinely different feasible
representation. Account for word boundaries, periodic wraparound, input and
output conversion, scratch state, and the cost of the whole epoch. Explain
what changes if each intermediate state must be returned or if masks change
after every step.
