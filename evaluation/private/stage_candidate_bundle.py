"""Copy only the public evaluation inputs and record a deterministic manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "evaluation" / "candidate"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new physical candidate-visible directory")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(PUBLIC.resolve()) or PUBLIC.resolve().is_relative_to(output):
        raise ValueError("candidate bundle output must be outside the repository's public source tree")
    if output.exists():
        raise FileExistsError(f"refusing to overwrite candidate bundle: {output}")
    shutil.copytree(PUBLIC, output, symlinks=False)
    records = []
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        records.append(f"{digest}  {path.relative_to(output).as_posix()}")
    (output / "MANIFEST.sha256").write_text("\n".join(records) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
