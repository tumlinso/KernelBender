# E04 — Transfer an algorithm across an architecture boundary

A Hopper implementation uses Tensor Memory Accelerator (TMA) to move regular
tiles from global memory into shared memory and uses an asynchronous barrier
to coordinate a producer and its consumers. The requested target is a V100
(`sm_70`) built with CUDA 12.9. The application may use public CUDA/C++ APIs
and documented `sm_70` instructions. It may not depend on Hopper headers,
driver-private interfaces, inline PTX for an unavailable Hopper instruction,
or a newer-GPU fallback at runtime. Preserve the tiled operator's values,
participation, and synchronization semantics.

Explain which computational intent transfers and which native mechanism does
not. Give a feasible public alternative for Volta, or state the precise
missing contract if the operation cannot be preserved. Identify the compiler,
API, participation, and numerical facts that need source verification before
implementation. Do not invent a Volta TMA equivalent.
