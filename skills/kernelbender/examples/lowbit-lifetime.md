# Example: what the direct-decoding loss does and does not tell us

**Status:** design interpretation of bounded KernelWiki evidence; alternative construction unmeasured.

KernelWiki compares a direct W4A16 SIMT consumer with decoding packed weights to FP16 followed by cuBLAS. Materialization wins its tested resident throughput cases, including repeated use. The report defines exact nibble packing, scale order, FP16 rounding and FP32 accumulation; those define the represented operator. [KW-LOWBIT]

Do not conclude that compressed weights or decoding near a consumer are inherently inferior. The experiment changed both decoding placement and the arithmetic engine. A specialized composed operation may offer another design: share decoding across two consumers, decode into their native operand ownership, or prepare a persistent tile representation on updates instead of returning to a canonical matrix.

The brief must state which cost it expects to remove and which it adds. If the caller's two consumers want incompatible fragments, sharing decode may increase routing and live state. If scale placement/rounding is specified, moving a scale across accumulation may violate semantics. If the weights change frequently, a retained decoded cache needs real invalidation and capacity.

A discriminating comparison should reuse the same decoded values and math policy, retain materialize+best-library and a supported native-compute alternative, and include preparation, conversion, both consumers and updates. It should not merely compare the old slow SIMT decoder to a new Tensor Core path and attribute every gain to fusion.

The broader lesson is to choose representations for the whole useful lifetime, while preserving the exact experimental boundary of prior wins and losses. Sources: [AT-R11], [AT-M25], [KW-LOWBIT].
