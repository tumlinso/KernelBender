# Retrieve the machine contract from KernelWiki

KernelBender describes a computation that might be built. Use [KernelWiki](https://github.com/tumlinso/KernelWiki) for the exact machine facts that make it legal and interpretable. Start with one architecture-filtered query, then fetch only the cited page and its sources:

```sh
python3 scripts/query.py --architecture sm70 --type hardware --compact
python3 scripts/get_page.py hw-volta-mma --follow-sources
```

For an Ampere target, substitute `--architecture sm80`; do not use an Ampere page to qualify Volta. The command paths are relative to the KernelWiki checkout. Page IDs are stable query selectors; source records identify the evidence behind them.

| Design question | Exact KernelWiki page ID | Target / why it matters |
|---|---|---|
| Explicit Volta MMA instruction coordinates, lane and slot ownership | `hw-volta-mma` | `sm70`; exact PTX form only. It does not define opaque WMMA raw storage. |
| Warp/CTA participation, barriers, memory ordering and progress | `hw-volta-participation` | `sm70`; choose the actual scope and required participants before using collectives or publication. |
| Volta tensor rounding and numerical observations | `hw-volta-numerics` | `sm70`; finite measurements are not a general arithmetic error bound. |
| Registers, shared memory, enabled product limits and occupancy constraints | `hw-volta-resources` | `sm70`; separate product resources from full-die capacity. |
| Feature eligibility and generation boundaries | `hw-volta-feature-boundaries` | `sm70`; check an exact target before importing a newer mechanism. |
| Volta operand reads, register banking, reuse and dependencies | `hw-volta-operand-delivery` | `sm70`; implementation measurements are not an ISA allocation contract. |
| Volta bitwise logic, byte selection, set-bit search, packed byte dot, and warp routing forms | `hw-volta-integer-routing` | `sm70`; exact PTX/API eligibility, mask and sentinel requirements, and signedness. |
| Public VMM reservation, mapping, access and granularity contracts | `hw-volta-vmm-addressing` | `sm70`; alias mapping does not establish concurrent visibility or coherence. |
| Explicit PTX MMA map validation for the tested form | `hw-volta-atlas-e09-mma-coordinate` | bounded campaign evidence; does not establish WMMA lane-to-fragment ownership. |
| Packed set-intersection comparison | `hw-volta-atlas-e11-packed-intersection` | bounded campaign evidence; one dense 16×16 output and actual iteration count one. |
| Independent small transform comparison | `hw-volta-atlas-e12-independent-transform` | bounded campaign evidence; four independent 4-variable blocks, not coupled `M^r x`. |
| Resident execution versus ordinary scheduling | `hw-volta-atlas-e16-resident-scheduling` | bounded campaign evidence; resident path lost to batching and graph replay in selected cases. |
| VMM alias versus ring baseline | `hw-volta-atlas-e23-vmm-aliasing` | bounded campaign evidence; both requested sizes mapped to the same 2 MiB logical domain; modulo was not isolated. |
| Bitplane versus native full-adder path | `hw-volta-atlas-e39-bitplane-addition` | bounded campaign evidence; native generally led, and the small bitplane median ordering had an interval crossing zero. |
| Asynchronous global-to-shared copy and pipeline constraints | `hw-ampere-async-copy` | `sm80`; Ampere capability, eligibility, waits/barriers and costs. Never infer this mechanism for `sm70`. |
| Ampere Tensor Core formats and sparse eligibility | `hw-ampere-tensor-operations` | `sm80`; precision and supported operation forms are target-specific. |
| Ampere L2/shared-memory and resource changes | `hw-ampere-memory-resources` | `sm80`; architecture-specific resource choices change staging economics. |

The six Volta campaign evidence pages are measured-evidence summaries, not generic hardware guarantees. Keep the workload and measured boundary attached to every inference. A query or page fetch is a lookup step, not an execution authorization.

## Access and confidence remain separate

Use the target page's stated source class and access boundary. A public CUDA/PTX capability, a source-reported implementation detail, a bounded observation, and a design hypothesis answer different questions. Driver/channel, binary-editing, firmware, graphics or platform-only observations are research leads; they do not become ordinary CUDA permissions because they appear in this library. For exact provenance and claim scope, follow the Wiki page to its sources.
