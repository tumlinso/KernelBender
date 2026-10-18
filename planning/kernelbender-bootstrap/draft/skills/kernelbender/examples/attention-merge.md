# Example: evidence selects a different ownership structure

**Status:** teaching case from an existing KDA study; not a KernelBender result or a held-out evaluation problem.

The KDA attention study examined a merge with a small grid and a dependent partial-vector accumulation. Its recorded source/SASS attribution pointed to the consumer region, while low DRAM throughput did not support a saturation explanation. A proposed revision loaded stable merge weights in parallel and distributed feature accumulation across more threads. The parent partial kernel, split count, precision and workload contract remained unchanged. [KDA-DIAGNOSIS]

The study's direct attribution record says the combined merge transformation is compared with its parent; the individual changes to weight calculation and feature ownership were not separately isolated. Fresh paired confirmation was against the stronger split16 baseline, not a separately confirmed parent promotion. Preserve those distinctions when teaching the result. [KDA-ATTRIBUTION]

The transferable reasoning is not “always use more threads” or a fixed register-count target. It is to inspect the entire partial+consumer path, identify which dependency/ownership choice limits useful work, and test a redesigned boundary without changing the mathematical state.

The study also found a shared-scratch race in a materialized baseline and rejected a numerically plausible mixed candidate after sanitizer failures. Seeded numerical checks did not make the race legal. Use corrected source and fresh identities for new comparisons. Do not claim an old profile/timing belongs to a repaired binary. [KDA-STUDY]

This is suitable as an instructional example because the mechanism and evidence limits are explicit. Reproducing it may check integration, but cannot establish that KernelBender creates new designs.
