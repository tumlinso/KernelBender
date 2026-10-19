# Consolidation validation

This report separates content/retrieval qualification from GPU implementation
or skill-effectiveness evidence. The consolidation does not run GPU experiments
and does not establish new performance results. The earlier native pilot in
`evaluation/REPORT.md` retains its original frozen skill and evidence scope.

## Starting point

Checked out on 2026-10-19 before implementation:

| Component | Revision | Initial state |
|---|---|---|
| KernelBender | `2af536a156999e37fee06b0535a002586eee4f47` | Clean |
| KernelWiki | `c9bf8dba49f2e5cf90c1dc9a78f970359da5ba5e` | Clean |
| Atlas | `5b5629b001da4a42d6f41a84d94f73c07a29d478` | Tracked files clean; untracked Todo metadata retained |
| Installed skills Git root | `0a6fab0ef005264a15b7c4d7b3cbb842bfdddfdf` | Untracked unrelated paths retained |
| Source skills workspace | `bfa9238985dfeb2368bad076f1cc51bfdadbae92` | Existing Todo and unrelated changes retained |
| KDA | `e1246674c5cbd47f5b535e21918b785a78a11363` | Clean |

KDA initially pins KernelBender `bcbba51e0ba3ebeac10f5bfda68832ccdcfc43cf`
and KernelWiki `244283cb8b57d1695af61aaa5e0cf5a04edfe9c9`.
No reset to those checkpoints is part of this work.

## Baseline commands and results

Commands run from the named repository root:

| Repository | Command | Result |
|---|---|---|
| KernelBender | `python3 -m unittest discover -s tests -v` | 22 tests passed before edits |
| KernelWiki | `python3 scripts/validate.py` | 1,078 files, 1,005 source IDs, 44 asset bundles, 14 ledgers; valid |
| KDA | `python3 -m unittest tests.test_kernelbender_consumer -v` | 1 test passed against existing pins |

The initial full KernelWiki command `python3 -m unittest discover -s tests -v`
ran 266 tests and found three failures and one error. Three assertions still
expected an August test count, only verbatim asset modes, or an obsolete literal
technique count in the skill. The fourth checked historical source closure
against current CUDA controller/profiler files whose hashes had already changed.
The consolidation's test maintenance must preserve historical identities and
explicit rejection of current-file drift, rather than rewrite receipts or
present that old GPU evidence as freshly qualified.

The retained Atlas passed these read-only source checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B scripts/test_atlas_suite.py
PYTHONDONTWRITEBYTECODE=1 python -B tools/test_campaign_evidence.py
PYTHONDONTWRITEBYTECODE=1 python -B tools/semantic_checks.py --output /tmp/atlas-consolidation-semantic-checks.json
```

Results: 24 tests, six tests, and 15 semantic groups containing 31,094 assertions,
respectively. These are portable/CPU checks, not new GPU observations.

The pre-existing CUDA embedded-bundle check
`python -B references/architectures/volta/v100_atlas/tools/sync_skill_bundle.py --validate`
failed against `assets/cuda-markdown-manifest.json` in its archived CUDA corpus
baseline. The original source was left untouched. See the provenance report
for exact hashes and the scope of the copy comparison.

## Reproducing paired validation

After running the individual repository suites, use an explicit compatible
KernelWiki checkout:

```sh
python3 tests/check_knowledge_pair.py --wiki ../KernelWiki
```

This read-only check resolves every exact hardware ID cited by the installed
skill, follows its source IDs, exercises the actual Wiki query filters, and
checks separation of SM70, neighboring SM72, and SM80. It does not install or
update a dependency. The component repositories remain independently usable.

Behavioral fixtures and their independent reasoning/CPU checks are retained
under `evaluation/atlas-consolidation/`. They are deliberately outside the
installed skill. They assess concrete constructions and rejection decisions;
they are not a matched comparison establishing incremental skill efficacy.

## Integrated checks

| Repository | Command | Result |
|---|---|---|
| KernelBender | `python3 /home/tumlinson/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/kernelbender` | Skill valid; the helper belongs to the installed skill-creator, not a runtime dependency |
| KernelWiki | `python3 scripts/generate-indices.py` | Seven query indices regenerated using the existing generator |
| KernelWiki | `python3 -m unittest discover -s tests -v` | 274 tests passed after all contract additions and baseline repairs |
| KernelWiki | `python3 scripts/volta_evidence_check.py --all` | Nine archived cases valid, zero errors; offline provenance qualification |
| KDA | `python3 -m unittest tests.test_core tests.test_engine tests.test_selection tests.test_kernelbender_consumer -v` | 29 CPU tests passed against unchanged existing pins |

The schema validator initially passed the integrated 1,093-page corpus with
1,009 source IDs, 44 asset bundles, and 14 ledgers. Final validation after the
integer/routing contract passed with 1,095 files, 1,010 source IDs, 44 asset
bundles, and 14 ledgers. The
independent content review led to that addition, a precise `.cg` cache-policy
qualification, and the Ampere structured-sparsity route. It also caught source
markers that were readable as citation keys but were not clickable Markdown;
the new library now links them to its local pinned-identity section.

The four previously failing Wiki tests were repaired without changing the
production evidence checker or archived receipt hashes. The archive test uses
the checker's existing portable mode and checks the frozen closure identity;
a separate deterministic negative test proves that live mode still rejects
a same-size toolchain file with a changed hash. This does not qualify the
current host as identical to the historical campaign environment.

## Source preservation and access

SHA-256 comparisons against a pre-edit snapshot found no changed tracked files
in the standalone Atlas (286 files), installed skills Git root (830), source
skills workspace (1,909), or KDA (68). Their Git status output also matched the
snapshot, including existing untracked/dirty state. The KDA submodule pins and
candidate evaluator were not edited. No GPU work, service restart, scheduler,
or publishing operation was required.

Public source URLs were checked with unauthenticated HTTP GETs and HTML
fragment checks where applicable. Atlas origin URLs returned 404 without
authentication; all pinned paths used by the migration resolved as local Git
objects at the recorded source revision. The documentation labels the access
boundary and gives `git -C <atlas-checkout> show <revision>:<path>` fallbacks.
These Atlas locators are not claimed to be publicly accessible. No new Wiki
file is linked through an unpublished GitHub commit: the installed skill uses
exact page IDs and the existing independent repository's retrieval commands.

## Final content and behavior results

- `python3 -m unittest discover -s tests -v` in KernelBender: **34 tests passed**.
- `python3 tests/check_knowledge_pair.py --wiki ../KernelWiki`: **17 exact
  hardware contract IDs resolved**, with actual architecture/confidence filters
  and source-ID closure checked.
- `python3 tests/test_consolidation_examples.py`: **seven CPU oracle checks
  passed** for the independent design fixtures.
- `sha256sum -c evaluation/atlas-consolidation/read-set-postrepair.sha256`:
  all three post-repair identities verified. The initial manifest intentionally
  retains three earlier hashes invalidated by concurrent reviewed edits.
- `python3 tests/check_migration_links.py --wiki ../KernelWiki --atlas ../gpu_circuit_bending_atlas --external`:
  2,469 local Markdown targets resolved; 23 introduced source URL bases checked;
  six public bases reachable (including the new official-guide fragment),
  17 access-gated Atlas locators resolved to pinned local Git objects; zero
  errors. Counts can increase when the delivery handoff adds local links.
- `git diff --check` passed in both component repositories.

The [independent behavioral run](../../evaluation/atlas-consolidation/blind-run-2026-10-19.md)
produced concrete graph, repeated-use predicate, and tensor/ownership briefs,
retained the conventional dense-library control, and rejected native SM70
`cp.async` while supplying a public fallback. The graph and repeated-use
examples compose several mechanisms rather than quote a stored operator.
The evaluator's tensor fixture originally omitted the scope of its sample
index; root caught the ambiguity, the fixture was clarified to four local
samples per warp group, and the report records that correction. This is a
fixture repair, not a skill success on the ambiguous original contract.

The [independent content review](REVIEW.md) found no remaining blocking defect
in its reviewed claims. Its failed optional pytest invocation is recorded
there; root's executed unittest suite is the test evidence, and no pytest pass
is claimed. Coverage remains bounded by [COVERAGE.md](COVERAGE.md). None of
these checks establishes GPU speedup, general skill effectiveness, or source
corpus retirement.

[SOURCE-PRESERVATION.json](SOURCE-PRESERVATION.json) retains the source-manifest
comparison digests and unchanged-state results. Both component commits will
be local only; no push or KDA dependency-pin mutation is part of this delivery.
