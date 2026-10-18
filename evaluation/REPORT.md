# KernelBender evaluation

Status: behavioral probes and the bounded native pilot complete. KernelBender remains optional and experimental.

Frozen skill: `25b4b167c73caf4f6540132013e10f58c0e43f73`. Evaluator freeze: `17072cb`.

Two matched fresh-context A/B blocks covered six design probes, using configured Luna implementer xhigh profiles, 300-second command sessions and at most twelve sandboxed commands per agent. The baseline had the current CUDA machine-aligned guidance and Atlas access; the treatment additionally read KernelBender.

The independent [behavior review](results/design-v1/REVIEW.md) finds useful guidance in both arms and no consequential failure requiring revision. Both arms reached the principal constructions. These observations do not establish incremental benefit or kernel performance. Treatment command-session intervals were longer in both blocks; model token costs were not available. Raw briefs, receipts, observed command costs, input hashes and source manifests are retained under `results/design-v1/`.

The command namespaces withheld repository/evaluator/other-arm files, network and GPU devices. Broader model tools remained instruction-constrained; this is not a hostile-agent blindness qualification. One treatment shell glob failed before wrapper entry without reading file contents, and one baseline read failed inside its namespace. Neither attempt was replaced.

The skill remains experimental. The native results below are task-local evidence; they do not establish incremental skill effectiveness.

## Native pilot

Run `kb-native-pilot-r4` used one fresh Luna A/B pair per family on a controller-admitted Tesla V100-SXM2-16GB, SM70, CUDA12.9/cuBLAS12.9, NumPy2.2.6 and Python3.13.11. All three baselines and six candidates passed memcheck, racecheck, public cases and independent private checks before timing. Complete caller-visible API wall time includes candidate allocation, preparation, updates and full-device completion. Host transfers/setup and output reset are outside timing. Frozen timing budget: two warmups, three samples, two exploration and two confirmation rounds.

| Family | A exploration speedup | B exploration speedup | Confirmed KDA decision |
|---|---:|---:|---|
| Boolean transition | 2.654x | 2.861x | B kernel promoted at 2.890x versus baseline (95% interval 2.747–3.008x). |
| Observable energy | 2.464x | 2.462x | Baseline retained: selected A confirmation had a 0.894x speedup on the one-use large case, below the frozen 0.9x floor. |
| Dense GEMM control | 1.054x | 1.052x | Baseline retained: confirmation 1.004x (0.961–1.048x) did not support the minimum improvement. Both arms retained baseline source byte-for-byte. |

These ratios compare each implementation with its task baseline, not a causal A/B skill-effect estimate. Both workflows produced useful specialized kernels. Dense-control exploration differences despite identical source illustrate timing noise. The Boolean B kernel is a task-local promotion; a single pair does not show that KernelBender caused its advantage. No skill-level win is claimed, no independent repeat or ablation was run, and the skill is not promoted to a default workflow.

All six agents produced a compiled final candidate within their matched caps. There were seven successful compile attempts: Boolean B compiled twice and superseded the first source after its own review. No candidate was retuned after GPU results. Recorded command-session intervals total 885.3 seconds (A 412.3, B 473.0); this is not a token-cost estimate. The three harness launch failures and all attempt sources are retained. They were controller path normalization, root selecting a Python without NumPy, and the evaluator's eager lookup of a legacy cuBLAS symbol. These failed before candidate CUDA execution; fixes applied equally without changing workloads or tolerances.

[Native result](results/native-pilot.json), [portable candidate evidence](results/native-v1/candidates/INDEX.json), [agent costs](results/native-v1/observed-agent-costs.json), [launch failures](results/native-v1/execution-attempts.json), and compact KDA/sanitizer evidence in `results/native-v1/retained-results/` record source, binary, workload, environment and controller identities. Full raw artifacts remain local under ignored `runs/` and `.todo-orchestrator/runtime/`; exported summaries reference those original paths. No profiler or cross-generation performance qualification was needed or claimed.

The installed generic sanitizer classifier labels clean racecheck logs partial because they use `RACECHECK SUMMARY` rather than `ERROR SUMMARY`. Qualification therefore requires the actual tool-specific zero-hazard/error/warning summary, target exit0 and independent validator, not that generic classification.
