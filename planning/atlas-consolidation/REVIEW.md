# Read-only consolidation review

## Decision

No blocking content or architecture defect remains in the reviewed migration after the latest fixes. The strongest ownership split is sound: KernelBender now routes integer, routing, and tensor design ideas to exact KernelWiki pages; KernelWiki keeps exact contracts and bounded experiment scope. KernelBender stays selective and does not take on execution/evaluation responsibilities.

## Findings, ranked

1. **Previously identified retrieval gaps are fixed.** KernelWiki now has `hw-volta-integer-routing`, including LOP3, PRMT, FNS, DP4A, DP2A, and warp-collective contracts. KernelBender's exact-contract map and bit-routing, arithmetic/tensor, and positional-routing cards point to that page. Its SM70 architecture filter returns the new record. Earlier undefined Atlas reference links also now resolve through the local `sources.md#atlas-identity` anchor.

2. **SM80 sparse wording is now appropriately scoped.** `hw-ampere-tensor-operations.md:32` distinguishes FP16/BF16 and int8 2:4 from TF32 1:2, says the two metadata-selected slots can carry zero values, and bounds lossless representation to at most two mathematical nonzeros per relevant group. It also says the instruction consumes encoded sparse data rather than discovering/compressing arbitrary dense zeros, requires the warp collective and valid metadata layout, and makes no performance claim. This matches the formats in PTX ISA 8.8 section 9.7.14.6.1 and the fragment/layout distinctions in 9.7.14.6.2. Exact selector and shape details remain delegated to PTX.

3. **The Volta MMA map and evidence boundary are correct.** `wiki/hardware/volta-mma.md:27-47` identifies the exact `m8n8k4` FP16-input/FP32-accumulator form, maps its A/B and accumulator elements, and states that the full warp executes the collective even though the mapping describes four independent products. It does not transfer the explicit PTX map to opaque WMMA fragments. E09 is limited to the explicit coordinate check; its WMMA subcase did not establish raw fragment ownership.

4. **Reviewed experimental records retain their actual scope.** The six detailed records preserve the requested boundaries: E09 explicit PTX coordinates only; E11 one tested dense 16x16 intersection with actual reuse count one; E12 independent blocks, not coupled recurrence; E16 resident scheduling lost in tested cases, not a general persistence rejection; E23 same rounded 2 MiB domain against a serial modulo baseline, without isolating modulo or establishing TLB/coherence claims; E39 native arithmetic generally led in selected cases, without an established bitplane crossover. The campaign index leaves other records at their source IDs rather than implying that every `GPU_RUN` protocol completed.

5. **Ampere and interface scope are handled carefully.** The new async-copy page distinguishes SM80 hardware acceleration from earlier API fallbacks, separates cache hints from ordering, and accounts for copy completion, consumer completion, pipeline buffers, and resource costs. `ampere-memory-resources.md` scopes values to SM80/A100 and cautions against treating capacities as residency/performance. Volta's VMM page covers public reservation/mapping/access/alias consistency and explicitly keeps driver/channel/firmware observations outside ordinary CUDA reachability.

6. **KernelBender contains useful generative constructions, not only an index.** The opportunity index routes by problem structure and pairs an affordance with a composition; the discrete-state, positional-routing, tensor-circuit, ownership, screening/refinement, phase-factoring, and system-composition cards give equations or ownership maps, a practical baseline, complete-path costs, and a falsifier. Dense-library controls and unfamiliar graph/discrete-state composition are present. I did not inspect the verifier's blind behavioral fixtures.

## Coverage limits and uncertainty

- The consolidation reports its intentional incompleteness. Packed SIMD conversion/saturation detail (M09), some topology/NUMA and non-SM/platform contracts, and many detailed experiment protocols remain with the pinned Atlas or primary CUDA sources. Ampere coverage is a useful SM80 route, not full CUDA-skill parity or replacement qualification.
- Raw Atlas samples/profiles are absent from the portable tracked summary. The Wiki records them as unavailable and retains a pinned local Git fallback; unauthenticated access to the Atlas GitHub locators was not assumed.
- I reviewed the targeted SM70 MMA/integer/VMM claims, SM80 async/Tensor Core/sparsity claims, six named experiments, and representative KernelBender retrieval/construction routes. This is not an independent audit of all 190 Atlas IDs or every KernelWiki page.
- I did not run GPU tests or inspect blind fixtures. `pytest` is not installed for the default `/home/tumlinson/Software/miniconda3/bin/python3`, so my focused pytest invocation could not run; root's broader suite results are separate evidence.

## Reproduction and validation evidence

From `/home/tumlinson/KernelWiki`:

```sh
python3 scripts/query.py --architecture sm70 --type hardware --tag dp4a --compact
python3 scripts/get_page.py hw-volta-integer-routing --follow-sources
python3 scripts/validate.py
git diff --check
```

The query returned exactly `hw-volta-integer-routing`. `get_page --follow-sources` returned the contract plus PTX 8.8, CUDA 12.9.1 guide, and CUDA Math API source records. The validator reported 1,095 valid files, 1,010 source IDs, 44 asset bundles, and 14 candidate ledgers; whitespace validation passed. A focused pytest command failed before collection with `No module named pytest`.

From `/home/tumlinson/KernelBender`:

```sh
git diff --check
```

Whitespace validation passed after the contract-route update. Root separately reports the full Wiki and KernelBender suites passing; I did not independently reproduce those full-suite runs.
