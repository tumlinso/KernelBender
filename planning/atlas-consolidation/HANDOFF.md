# Independently versioned consolidation handoff

## Qualified component revisions

| Component | Exact implementation revision |
|---|---|
| KernelBender | `96b3ee5fb9fa4eca00d452854d4a3e035b1d1906` |
| KernelWiki | `68c017a443eb7970bcfb39660e553cd68152db7b` |

The follow-up KernelBender commit containing this handoff changes delivery
documentation only. Its runtime skill, fixtures and tools are identical to the
qualified implementation revision above. Both repositories are independently
versioned; no Git push was performed. These commits can be obtained from the
local repositories. Remote submodule URLs will not contain unpublished commits
until separately authorized publication.

## Delivered capability

KernelBender retains its ten bridges and selective design-brief interface,
adding four affordance families, eight composition families, problem-first
routes, an exact Wiki contract map, and a conventional dense-library control.
The [crosswalk](CROSSWALK.md) accounts for all 190 R/M/C/E/S IDs; it distinguishes
active construction/fact/evidence ownership from intentionally retained source
material. [Coverage](COVERAGE.md) and [provenance](PROVENANCE.md) record the
remaining gaps and license/access limits.

KernelWiki enriches six Volta pages, adds exact integer/routing and public VMM
contracts, preserves six detailed bounded observations and the forty-experiment
status index, and establishes source-backed SM80/A100 copy, dense/sparse tensor,
and resource routes. Its existing schema/query APIs remain in use. No knowledge
database, profiler, optimizer, orchestrator, candidate evaluator or GPU scheduler
was added.

## Validation and limits

The [validation report](VALIDATION.md) contains commands, baseline failures and
their repairs, final results, source preservation, and external availability.
Results: 34 KernelBender tests, 274 Wiki tests, 1,095 valid Wiki pages,
17 paired hardware contracts, nine archived evidence cases, 29 existing KDA CPU
tests, and seven CPU oracles for five independent design fixtures. The
[behavioral report](../../evaluation/atlas-consolidation/blind-run-2026-10-19.md)
retains concrete designs, conventional/unsupported controls, initial routing
failures and the evaluator fixture correction. The [content review](REVIEW.md)
found no remaining blocking defect within its stated coverage.

These checks do not establish new GPU performance, general skill effectiveness,
or retirement qualification. Most full experiment protocols, detailed packed
SIMD and some topology/platform contracts remain with retained sources. Atlas
URLs are access-gated; exact local Git source fallbacks are provided. No Atlas
prose or artifacts were vendored and no repository license was selected for
KernelBender.

## Optional KDA integration

KDA remains unchanged at `e1246674c5cbd47f5b535e21918b785a78a11363`, with its
existing KernelBender `bcbba51e0ba3ebeac10f5bfda68832ccdcfc43cf` and KernelWiki
`244283cb8b57d1695af61aaa5e0cf5a04edfe9c9` pins. Existing CPU consumer/core/
engine/selection checks passed 29/29. A temporary staging tree containing the
unchanged KDA prompt/test and the proposed KernelBender skill passed the same
consumer test (one test); no KDA file or gitlink was edited.

If pin updates are later authorized, the expected integration is a separate
commit changing only `skills/KernelBender` and `skills/KernelWiki` gitlinks.
The entry remains `skills/KernelBender/skills/kernelbender/SKILL.md`; Wiki
commands and page-ID retrieval remain unchanged. No prompt rewrite, Atlas
import, database import or `kda_experiments` modification is required.

From KDA, the existing CPU consumer check is:

```sh
python3 -m unittest tests.test_core tests.test_engine tests.test_selection tests.test_kernelbender_consumer -v
```

From KernelBender, validate any selected pair before pinning:

```sh
python3 -m unittest discover -s tests -v
python3 tests/check_knowledge_pair.py --wiki ../KernelWiki
python3 tests/check_migration_links.py --wiki ../KernelWiki --atlas ../gpu_circuit_bending_atlas --external
```

The original Atlas, installed CUDA skill, source skills workspace, and KDA
tracked bytes and existing Git states were preserved, as recorded in
[SOURCE-PRESERVATION.json](SOURCE-PRESERVATION.json). No service restart or GPU
execution was needed.
