#!/usr/bin/env python3
"""Read-only cross-repository acceptance check; neither repo is a dependency.

Run after the component suites, with an explicit compatible KernelWiki clone:
    python3 tests/check_knowledge_pair.py --wiki ../KernelWiki
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path, required=True)
    args = parser.parse_args()
    wiki = args.wiki.resolve()
    scripts = wiki / "scripts"
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location("paired_wiki_query", scripts / "query.py")
    if spec is None or spec.loader is None:
        raise SystemExit("Cannot load the selected KernelWiki query implementation")
    query = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(query)
    pages = query.load_all_pages()
    by_id = {page["fm"].get("id"): page for page in pages}
    skill = Path(__file__).resolve().parents[1] / "skills" / "kernelbender"
    routes = skill / "references" / "wiki-contracts.md"
    ids = set(re.findall(r"\bhw-[a-z0-9]+(?:-[a-z0-9]+)+\b", routes.read_text()))
    if not ids:
        raise AssertionError("No exact Wiki contracts registered")
    missing = ids - by_id.keys()
    if missing:
        raise AssertionError(f"Missing Wiki contract IDs: {sorted(missing)}")
    referenced = set()
    for path in skill.rglob("*.md"):
        referenced.update(re.findall(r"\bhw-[a-z0-9]+(?:-[a-z0-9]+)+\b", path.read_text()))
    if referenced - ids:
        raise AssertionError(f"Unregistered Wiki contracts: {sorted(referenced - ids)}")

    def selected(architecture: str, confidence: str | None = None) -> set[str]:
        filters = SimpleNamespace(type="hardware", tag=None, repo=None, language=None,
                                  architecture=architecture, symptom=None,
                                  confidence=confidence, has_code=False)
        return {page["fm"]["id"] for page in query.filter_pages(pages, filters)}

    v100 = selected("V100")
    if v100 != selected("sm70"):
        raise AssertionError("V100 alias disagrees with exact SM70 retrieval")
    checked = []
    for pid in sorted(ids):
        page = by_id[pid]
        fm = page["fm"]
        architectures = fm.get("architectures") or []
        confidence = fm.get("confidence")
        if not confidence or not fm.get("sources"):
            raise AssertionError(f"{pid}: missing confidence or sources")
        for sid in fm["sources"]:
            if sid not in by_id:
                raise AssertionError(f"{pid}: unresolved source {sid}")
        for architecture in architectures:
            if pid not in selected(architecture, confidence):
                raise AssertionError(f"{pid}: not returned under its own filters")
        if architectures == ["sm70"]:
            if pid not in v100 or pid in selected("sm72") or pid in selected("A100"):
                raise AssertionError(f"{pid}: exact SM70 eligibility leaked")
        if architectures == ["sm80"]:
            if pid not in selected("A100") or pid in v100:
                raise AssertionError(f"{pid}: exact SM80 eligibility leaked")
        checked.append({"id": pid, "architectures": architectures,
                        "confidence": confidence, "source_ids": fm["sources"]})
    print(json.dumps({"registered_contracts": len(ids),
                      "all_runtime_contract_references_resolve": True,
                      "contracts": checked}, indent=2))


if __name__ == "__main__":
    main()
