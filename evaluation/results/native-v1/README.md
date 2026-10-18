# Native pilot driver

This host-bound evaluator driver connects the frozen design trials to KDA's
existing candidate engine. `prepare` materializes the three accepted task
contracts, snapshots the corrected baselines and ready A/B candidates, and
builds them through KDA on CPU. `qualify` is reserved for the root-bound KB-06
gate: it controller-admits Compute Sanitizer and the public/private correctness
runner for each build before submitting only qualified candidates to KDA's
paired evaluator. A baseline qualification failure blocks its family. A failed
or absent treatment remains recorded and receives no timing.

The candidate map is JSON schema version 1. It binds the frozen trial policy
and shared design-source manifest and requires explicit A/B outcomes and
retained trial receipts/command logs:

```json
{
  "schema_version": 1,
  "run_id": "kb-native-pilot-1",
  "trial_policy_sha256": "<sha256 of design-v1/trial-policy.json>",
  "source_manifest_sha256": "<sha256 of design-v1/shared-source-manifest.json>",
  "agent_policy_sha256": "<sha256 of native-v1/agent-policy.json>",
  "input_manifests_sha256": "<sha256 of native-v1/input-manifests.json>",
  "families": {
    "bool-transition": {
      "A": {
        "trial_id": "bool-A",
        "outcome": "candidate_ready",
        "build_attempts": 1,
        "candidate_source": {"source_dir": "/staged/bool-A", "manifest": "manifest.json"},
        "attempt_records": [
          {"kind": "receipt", "path": "/staged/bool-A/receipt.json", "sha256": "<sha256>"},
          {"kind": "commands", "path": "/staged/bool-A/commands.jsonl", "sha256": "<sha256>"}
        ]
      },
      "B": {
        "trial_id": "bool-B",
        "outcome": "no_candidate",
        "build_attempts": 0,
        "candidate_source": null,
        "attempt_records": [
          {"kind": "receipt", "path": "/staged/bool-B/receipt.json", "sha256": "<sha256>"},
          {"kind": "commands", "path": "/staged/bool-B/commands.jsonl", "sha256": "<sha256>"}
        ]
      }
    }
  }
}
```

Repeat the explicit A/B records under the other two family keys. `outcome` is
`candidate_ready`, `no_candidate`, or `failed`; `candidate_source` is present
only for a ready candidate. Per-arm `build_attempts` cannot exceed the frozen
two-build limit. `attempt_records` may also retain `briefs` and `other` files.
The driver copies all listed evidence and ready sources into the unique run
directory, hashes the copies, and registers the copied source with KDA.

Run the CPU preparation only after the root has staged the map:

```bash
python3 evaluation/results/native-v1/driver.py prepare \
  --run-id kb-native-pilot-1 --candidate-map /path/to/candidate-map.json
```

After the root binds the driver source and command to the required controller
gate, its execution command is:

```bash
python3 evaluation/results/native-v1/driver.py qualify --run-id kb-native-pilot-1
```

The driver runs memcheck and racecheck for each candidate using the selected
native trial policy. It uses the ignored site config under
`runs/kernelbender-pilot/site/controller.json`, the existing site controller
entry/runtime identity, and the CUDA 12.9 sanitizer policy adapter. Sanitizer
calls each receive one controller admission. KDA evaluation uses the task's
existing KDA launcher admission; the driver does not wrap it in a second
controller. The selected sanitizer tool, adapter and executable hashes,
controller receipt, raw log, summary, validator JSON, source snapshot, build
fingerprint and binary hashes are retained in the ignored run workspace.

This host-specific driver is evaluator material, not part of the installed
skill or candidate-visible task bundle. Folder separation alone is not an
access-control boundary; trial staging must continue to use the root's fresh
candidate contexts and constrained source mounts.
