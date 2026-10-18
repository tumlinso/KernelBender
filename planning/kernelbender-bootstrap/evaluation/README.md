# Evaluation assets — reviewer/evaluator material

This directory is not installed with the runtime skill. It defines independent assessment tasks and expected failure boundaries, not a library of candidate answers for the design agent.

`scenarios.json` contains six compact probes and task-family templates. Follow `design/EVALUATION.md` for the matched-stack protocol. The implementing evaluator creates frozen workload/precision contracts and independent oracles using the actual KDA interface. No results are prefilled and no model/GPU evaluation was performed for this delivery.

Keep evaluator notes, holdout seeds/results and alternative-arm transcripts outside candidate-readable task inputs. In an ordinary shared filesystem this needs a deliberately prepared task workspace or existing sandbox scope; naming a directory `private` is not access control. Do not build a new sandbox service for this pilot.

Actual receipts belong in the existing task run directories; commit compact results and their source identities, not private raw archives by default. Record a corrected baseline's new identity and do not inherit earlier unsafe timings.
