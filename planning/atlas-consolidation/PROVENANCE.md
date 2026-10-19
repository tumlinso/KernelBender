# Source identity, licensing, and validation provenance

## Source checkouts

| Repository | Checkout identity observed | State / relevance |
|---|---|---|
| Standalone Atlas | /home/tumlinson/gpu_circuit_bending_atlas, branch main, HEAD 5b5629b001da4a42d6f41a84d94f73c07a29d478; tree 1ee7066ad5e46210b49cb8f708d2c083bfb62bfa | Tracked tree clean. Existing untracked Todo metadata was left untouched. This is the source pin for every Atlas ID in CROSSWALK.md. |
| KernelBender | /home/tumlinson/KernelBender, HEAD 2af536a156999e37fee06b0535a002586eee4f47 at inventory start | Worktree already contained authorized concurrent consolidation edits. This inventory owns planning/atlas-consolidation/CROSSWALK.md, COVERAGE.md, and PROVENANCE.md only. |
| KernelWiki | /home/tumlinson/KernelWiki, HEAD c9bf8dba49f2e5cf90c1dc9a78f970359da5ba5e at inventory start | Clean at inspection; parallel implementation may add pages after that point. Use the resulting Wiki commit reported by the integration handoff, not this snapshot, as the final pin. |
| CUDA skill development checkout | Git root /home/tumlinson/skills_dev, branch development, HEAD bfa9238985dfeb2368bad076f1cc51bfdadbae92 | Atlas copy is cuda/references/architectures/volta/v100_atlas. Existing Todo projection and related scratch changes were present and left untouched. |
| Installed skills checkout | Git root /home/tumlinson/.agents/skills, HEAD 0a6fab0ef005264a15b7c4d7b3cbb842bfdddfdf | Atlas copy is cuda/references/architectures/volta/v100_atlas. No source changes were made. |

The standalone source identity was cross-checked against its Git tree and
manifest. Key SHA-256 values at the pinned source revision are:

- manifest.json: 687e913e88e238b496757c5dc606a393a49b21b306fc810d02ebed0b2efd4e8c
- SHA256SUMS: 23434ed437c2d8ceec440bb4cb7cda280fc61f2e06e78d2b839899884682016f
- experiments/CLAIM_LIMITS.md: b5fa423f537a0816e487633cbb2ba790e783af3da8593649dfd0423ad1c48e82
- experiments/INTERPRETING_RESULTS.md: 186a642c862aeff2e1e712a4962dd36f2dd0f84ece80f4303aed47f9c349b94d
- sources/SOURCES.md: b8601336afec9be100e7ee0f791fe3771c8cd90be89a896d280d1ca86ce4ed1a

The source commit history distinguishes original design authoring from later
campaign work: original experiment cards were committed at
5c1f805db80a81f7476ede8292abba69821d104f; campaign implementation/source
updates are represented by f223c51dcfacab602e9bc68b3e65cc75730dc7f8; the
current consolidated source is 5b5629b001da4a42d6f41a84d94f73c07a29d478.
The campaign identifier is v100-20261006T145155Z-4bd01216 and its key is
7beacfbd95e0d2b8f9725c7ba1477122f16bc1eb686a6a7c94dbf6c7e266794b.

## Copies and access

The CUDA development and installed skill copies are byte-identical to each
other across 600 files. Their import metadata pins Atlas revision
5b5629b. The 16 R cards, 52 M cards, 40 C cards, and 42 S cards match the
standalone source bytes. The 40 E cards match after the documented portable
path localizations for the campaign report, semantic-check tool, and
host-specific raw evidence. Stable IDs are preserved. This establishes copy
identity for the compared files; it does not make an embedded copy the
authority for later Atlas revisions.

An unauthenticated HTTP GET to the Atlas GitHub origin and the raw
CLAIM_LIMITS.md URL returned 404 during this review. KernelWiki's origin and
documentation returned 200. Treat the Atlas as locally available at its pinned
Git commit, with external unauthenticated access gated or unavailable. A 404
does not establish corruption or a missing local source. For reproducible
local access, use:

    git -C /home/tumlinson/gpu_circuit_bending_atlas show 5b5629b001da4a42d6f41a84d94f73c07a29d478:experiments/CLAIM_LIMITS.md

The crosswalk uses local Git identity and Atlas IDs; it does not depend on
public Atlas URLs. Any KernelWiki links to the origin should label this access
limitation and provide a local pinned-source locator.

## Copyright and license boundary

At the inspected revisions, neither standalone Atlas nor KernelBender has a
tracked LICENSE, COPYING, NOTICE, or AUTHORS grant selecting terms for
substantial redistribution. KernelWiki has a tracked MIT license attributed to
hanlab. The Atlas and KernelBender Git history identifies Gavin Tumlinson as
author of the relevant Atlas and KernelBender commits, but that is not itself a
license grant. Atlas source capsules are authored summaries and locators; the
linked third-party works keep their own terms.

The user authorized consolidation of the material, but that does not resolve
repository redistribution terms for copied prose, source snapshots, or
artifacts. The conservative implementation uses newly authored synthesis,
preserves Atlas IDs and attribution/provenance, links to exact local source
identity, and does not copy Atlas prose, benchmark binaries, raw evidence,
source capsules, or the full Atlas archive. Hardware facts are restated with
their primary/KernelWiki authority rather than maintained as duplicate
specifications. This is an implementation boundary, not legal advice and not a
license determination. No repository license was added or changed.

## Evidence interpretation

The manifest is dated 2026-10-03 and campaign run is dated 2026-10-06. Some
reference and experiment prose records the earlier authoring-time absence of a
GPU campaign; the later campaign status overlay records subsequent bounded
work. Both histories are retained. Do not read an old “not run at authoring”
statement as contradicting a later implemented subset, or read GPU_RUN as
completion of the originally proposed experiment.

The pinned campaign reports 29 GPU_RUN, 6 CPU_ONLY, and 5 NOT_RUN experiment
summaries. The required interpretation sources are:

- experiments/CLAIM_LIMITS.md at the hash above.
- experiments/INTERPRETING_RESULTS.md at the hash above.
- experiments/evidence/v100-20261006/provenance.json and the per-ID JSON
  summaries at the pinned source revision.

The portable campaign summary is tracked, but raw timing vectors, profiler
captures, and controller logs referenced by local host paths are not all
present in Git. Do not manufacture a reproducer or stronger claim from a
summary alone. E09 proves a map for one explicit PTX form, not raw WMMA
ownership. E11's requested reuse sweep did not run; its effective iterations
were one. E12 covers independent local blocks, not a coupled recurrence. E16
is a bounded scheduling comparison, not a starvation proof. E23 compares a
fixed alias walk with one serial modulo baseline, not an optimized general
ring. E39 finds native arithmetic generally lower in tested cases and no
statistical bitplane crossover. E27–E30 are unrun restricted-interface
hypotheses; public E32 and PTX E37 cases do not validate them.

## Commands run against the Atlas source

The following checks were safe offline contract/identity tests. They used
temporary directories for fixtures and no GPU:

| Exact command (working directory /home/tumlinson/gpu_circuit_bending_atlas) | Result |
|---|---|
| PYTHONDONTWRITEBYTECODE=1 python -B scripts/test_atlas_suite.py | PASS; 24 tests in 0.065 s. |
| PYTHONDONTWRITEBYTECODE=1 python -B tools/test_campaign_evidence.py | PASS; 6 tests in 0.007 s. |
| PYTHONDONTWRITEBYTECODE=1 python -B tools/semantic_checks.py --output /tmp/atlas-consolidation-semantic-checks.json | PASS; 15 test groups, 31,094 assertions, gpu_measured=false. |

The semantic checker defaults to a repository ledger output, so the command
explicitly redirected its result to /tmp. The source worktree remained tracked
clean, with only the pre-existing untracked Todo metadata. No GPU experiment,
source edit, test-generated repository artifact, or Project Control operation
was performed.

The CUDA bundle validator was also inspected, not repaired. In
skills_dev/cuda, this command failed:

    python -B references/architectures/volta/v100_atlas/tools/sync_skill_bundle.py --validate

It reported: “pre-existing CUDA resource hash changed without matching
content: cuda-resource-fdc0b9ba4e352fba9c02eac90d710c3284bd8f817bcd6ae75943f37e2461294e”.
At script lines 731–741, this check compares the existing resource record for
assets/cuda-markdown-manifest.json against
references/architectures/volta/v100_atlas/archive/cuda-corpus-baseline-9cafc69.source.json.
The baseline digest is
f1aa15dd8525629fa5b2cefdef6f589ea1307a9507954ab35ee3bfc1dbbae928, the
current .project-control-corpus.json record says
fe8f869fed9c83f5636919bc3cd9928506e610c6232c3f881e469f21450cd8d3, and the
actual asset digest is
7ca739e423bcf5d4e8abd95a0572a2c3ec48347930cea987b89e77df1d77bf11.
This is a mismatch in pre-existing CUDA-corpus baseline/resource metadata, not
an Atlas-card mismatch. No attempt was made to regenerate or edit the baseline.
