# Example: the consumer does not need the intermediate

**Status:** derived illustrative design; no GPU measurements.

A caller repeatedly receives X with B rows and K features. It currently computes `H=XW`, then `Y=HV`, where W is K×N and V is N×J, J is small, and W/V are unchanged across many calls. Only Y is observable.

The conventional route optimizes two GEMMs or fuses their boundary. KernelBender should first notice the *observable*: H is not required. If the numerical contract permits reassociation, prepare `C=WV` on parameter update and use `Y=XC` thereafter. The preprocessing performs approximately `2KNJ` real arithmetic operations; each query performs `2BKJ`, rather than `2BKN+2BNJ`. These are operation counts, not timing predictions.

The correct design brief also challenges its own prerequisites. If H is explicitly rounded to FP16 between stages, `(XW)V` and `X(WV)` do not generally implement the same finite-precision operator. If W/V update every call, preparation may dominate. If the application must return H or apply a nonlinearity to it, the simple elimination is unavailable. If low-rank structure is only approximate, it cannot become an exact invariant without authorization.

A useful first comparison has the same input distribution and allowed error policy, the strongest two-stage library baseline, the prepared path, an independent high-precision reference and both short- and long-lived parameter epochs. Measure update+uses+required output, not only the new small GEMM.

This example is deliberately not tied to attention or a matrix recipe. The transferable idea is to move a fixed consumer into preparation when doing so preserves the actual observable contract. Sources: [CUDA-MAD], [AT-R11], [MIRAGE].
