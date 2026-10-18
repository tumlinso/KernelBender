"""Stage the reviewed CUDA baseline as an ordinary KDA candidate source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
NATIVE = ROOT / "evaluation" / "candidate" / "native"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=("bool-transition", "observable-energy", "dense-gemm"))
    parser.add_argument("output", type=Path, help="new baseline candidate source directory")
    args = parser.parse_args()
    source = NATIVE / args.family
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to overwrite a non-empty candidate source directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / "baseline" / "kernel.cu", output / "kernel.cu")
    shutil.copyfile(source / "candidate_api.h", output / "candidate_api.h")
    manifest = {"schema_version": 1, "files": ["candidate_api.h", "kernel.cu"], "dependencies": []}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
