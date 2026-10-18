# Native pilot contracts

All three tasks target V100 (`sm_70`) with CUDA 12.9. Inputs and outputs are
device-resident FP32 or byte arrays; candidate functions receive a CUDA stream
and may use caller-created cuBLAS handle where stated. The operation runs once
per invocation, and the harness measures its full GPU work and host-call
overhead. Input creation and host-to-device transfer are outside this
resident-operator objective. Scratch allocation, packing, preparation,
conversion, synchronization, and output production performed by a candidate
are inside the measured call.

The `cases.json` files are the public fixed workloads. Each task's
`TASK.md` gives the exact contract. The evaluator materializes a KDA v1 task
manifest from these cases with `evaluation/private/materialize_tasks.py`.
The generated task and all site paths stay in the private evaluator workspace;
the candidate bundle contains no runner, reference, holdout, controller config,
or evaluator notes.

For an authorized local evaluator, materialize each task with the site's
controller config, the KDA checkout, and the explicit CUDA 12.9 compiler and
library directory. The script prints the generated `task.json` path. It does
not run KDA or acquire a GPU. The candidate source must contain top-level
`kernel.cu` and a copy of `candidate_api.h`; compile and benchmark commands are
owned by the trusted runner.

Register the supplied `baseline/kernel.cu` first as the incumbent in a fresh
KDA task workspace. Copy its matching `candidate_api.h` beside the source and
include both files in the candidate manifest. Both A and B receive the same
corrected baseline source. `evaluation/private/stage_baseline.py` stages that
source in the exact candidate layout and writes a KDA manifest. A design
paragraph is not a registered candidate.
