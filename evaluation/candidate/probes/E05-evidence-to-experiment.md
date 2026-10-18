# E05 — Separate an observation from its causal explanation

The following is a **constructed review fixture**, not hardware measurement.
An incumbent composed operator is labelled `A`; candidate `B` is 18% slower
in the fixture's ordinary end-to-end timing. One profiler replay reports 31%
fewer global bytes for `B`, 1.7x as many issued instructions, and twice as
many registers per thread. The source also contains a dependent consumer and
an irregular branch. A known race was found in an earlier version of `A`; the
current incumbent's race status has not been checked. No counter-to-source
attribution or sanitizer result is supplied.

Propose the next construction or controlled experiment. State what is
observed, what remains a hypothesis, how the unsafe earlier baseline affects
the comparison, and what evidence would distinguish low useful parallelism
from conversion/issue cost. Do not treat profiler replay duration as normal
throughput and do not prescribe a wall of unrelated tuning guesses.
