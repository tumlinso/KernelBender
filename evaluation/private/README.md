# Private evaluator workspace

`native_runner.py` and `references.py` are trusted inputs for the three KDA
native tasks. `holdouts.json` adds unadvertised validation cases; the
observable-energy runner applies `updated_w_seed` by uploading new weights and
calling the same loaded candidate function a second time in the same process.
`materialize_tasks.py` creates a KDA v1 task from one public `cases.json` and
injects the site's controller, KDA, CUDA compiler, and library paths. Generated
task manifests belong outside candidate-visible mounts. KDA hashes the declared
trusted inputs and copies them into each attempt's retained evidence.

`stage_baseline.py FAMILY OUTPUT` creates the identical baseline source layout
for both arms. `stage_candidate_bundle.py OUTPUT` physically copies only
`evaluation/candidate/` and writes a sorted SHA-256 manifest; it refuses to
overwrite a prior bundle. An evaluator should expose this copy read-only to
both arms and keep this `private/` tree, generated KDA tasks, the other arm, and
result/evidence directories outside candidate mounts.

The verified site launch uses an enforced read-only task/source mount, a
writable work mount, and no GPU or network mount for design sessions. This
limits filesystem visibility for commands inside that sandbox. It does not
prove that every model-side tool or host integration obeys the same boundary;
report any broader access that is not independently confined, and do not claim
hostile-agent blindness from directory naming or prompting alone. GPU
validation and timing must go through the site's existing KDA launcher and
controller admission path.

No runner in this directory has been executed against a GPU as part of KB-04.
The KDA baseline `prepare` check compiles and hashes candidate libraries only;
it does not establish correctness or performance. Before any timing result is
used, the controller owner must run all public and private correctness cases,
including the U=64 energy case and a memory/race sanitizer pass, under admitted
V100 execution.
