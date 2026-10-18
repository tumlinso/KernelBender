# KernelBender implementation handoff

KernelBender is an implemented, optional experimental instruction/reference skill. Use `skills/kernelbender/SKILL.md` for a structural kernel-design question; install or stage only `skills/kernelbender/`. In KDA the explicit entry is `skills/KernelBender/skills/kernelbender/SKILL.md`. Recursive skill discovery is not assumed. The calling agent retains task semantics, implementation, independent correctness checks, profiling and promotion authority.

## Version and evidence

The runtime tree is frozen at `25b4b167c73caf4f6540132013e10f58c0e43f73`; tested evaluator code is `7ed99082e0523af1ee6be569fd8c1e118c6cdf52`. Final documentation and evidence commits preserve that runtime tree. The KDA integration receipt records the exact consumed repository commit and gitlink.

The delivered package contains ten mechanism bridges, four worked examples, a selective caller route and a concrete design-brief template. It complements KDA, the CUDA skill, KernelWiki, ncu-report-skill and the Circuit-Bending Atlas. Evaluation material is outside the installed skill.

Validation passed: 22 CPU package/reference checks, 10 pilot-driver checks, the skill metadata validator, and the original bootstrap manifest checks. Six design probes were reviewed in two matched fresh-context A/B blocks. They did not establish incremental benefit over the competent CUDA/Atlas workflow.

The bounded native run `kb-native-pilot-r4` used one independent A/B pair per family on V100 SM70 with CUDA/cuBLAS12.9. All three baselines and six candidates passed controller-admitted memcheck/racecheck plus independent public/private correctness checks. KDA promoted the Boolean B kernel at 2.890x versus its baseline; it retained the energy baseline under the per-case regression rule and the dense GEMM baseline after confirmation. This is task-local kernel evidence, not a causal skill-level win. No independent agent repeat or ablation was run. KernelBender remains explicit and experimental.

See [evaluation report](../evaluation/REPORT.md), [native result](../evaluation/results/native-pilot.json), [candidate sources and all seven compile attempts](../evaluation/results/native-v1/candidates/INDEX.json), and [consumer checks](component-consumer-results.md). Three pre-workload harness failures are retained. Full raw binaries and controller/KDA artifacts remain local under ignored experiment/runtime paths; portable candidate sources, hashes, summaries and independent review are versioned.

## Minimal KDA consumption

Pin this independent repository at `skills/KernelBender`; add the explicit optional entry to the existing prompt and workflow documentation. Keep the brief in the task's existing `docs/draft.md`, then use KDA's current candidate registration and evaluator. No engine fields, numerical contracts, trusted evaluator policy, unrelated submodule pins or execution controls change. The companion native KDA task owns that integration and its regressions.

Future work should be a small, separately authorized investigation: independent paired agent repeats before any skill-level promotion claim, or a concrete caller-driven refinement. The current pilot does not justify broader activation or an architecture framework.
