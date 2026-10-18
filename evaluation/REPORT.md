# KernelBender evaluation

Status: behavioral probes complete; native pilot not yet run.

Frozen skill: `25b4b167c73caf4f6540132013e10f58c0e43f73`. Evaluator freeze: `17072cb`.

Two matched fresh-context A/B blocks covered six design probes, using configured Luna implementer xhigh profiles, 300-second command sessions and at most twelve sandboxed commands per agent. The baseline had the current CUDA machine-aligned guidance and Atlas access; the treatment additionally read KernelBender.

The independent [behavior review](results/design-v1/REVIEW.md) finds useful guidance in both arms and no consequential failure requiring revision. Both arms reached the principal constructions. These observations do not establish incremental benefit or kernel performance. Treatment command-session intervals were longer in both blocks; model token costs were not available. Raw briefs, receipts, observed command costs, input hashes and source manifests are retained under `results/design-v1/`.

The command namespaces withheld repository/evaluator/other-arm files, network and GPU devices. Broader model tools remained instruction-constrained; this is not a hostile-agent blindness qualification. One treatment shell glob failed before wrapper entry without reading file contents, and one baseline read failed inside its namespace. Neither attempt was replaced.

The skill remains experimental. Native implementation and controller-admitted correctness/sanitizer/timing comparisons follow the frozen protocol; no device or effectiveness result is claimed here.
