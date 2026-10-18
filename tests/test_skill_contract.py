"""Portable contract checks for the installed KernelBender skill tree."""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY / "skills" / "kernelbender"


def _frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"missing YAML frontmatter in {path}")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def _runtime_markdown_files() -> list[Path]:
    return sorted(SKILL_ROOT.rglob("*.md"))


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_has_required_discovery_fields(self) -> None:
        metadata = _frontmatter(SKILL_ROOT / "SKILL.md")
        self.assertEqual("kernelbender", metadata.get("name"))
        description = metadata.get("description", "")
        self.assertTrue(description)
        self.assertLessEqual(len(description), 1024)

    def test_runtime_markdown_links_resolve_inside_the_skill(self) -> None:
        broken: list[str] = []
        for source in _runtime_markdown_files():
            text = source.read_text(encoding="utf-8")
            for raw_target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
                target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                destination = (source.parent / unquote(parsed.path)).resolve()
                if not destination.exists() or not destination.is_relative_to(SKILL_ROOT.resolve()):
                    broken.append(f"{source.relative_to(REPOSITORY)} -> {target}")
        self.assertEqual([], broken)

    def test_cited_source_keys_have_exact_locators(self) -> None:
        source_text = (SKILL_ROOT / "references" / "sources.md").read_text(encoding="utf-8")
        known = set(re.findall(r"^\| ([A-Z][A-Z0-9-]+) \|", source_text, re.MULTILINE))
        known.update(re.findall(r"^\*\*([A-Z][A-Z0-9-]+) —", source_text, re.MULTILINE))

        cited: set[str] = set()
        citation = re.compile(r"\[([A-Z][A-Z0-9-]*(?:\s*,\s*[A-Z][A-Z0-9-]*)*)\]")
        for source in _runtime_markdown_files():
            for group in citation.findall(source.read_text(encoding="utf-8")):
                cited.update(key.strip() for key in group.split(","))
        self.assertEqual(set(), cited - known)

    def test_clean_codex_home_staging_contains_only_the_skill(self) -> None:
        source_files = {
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertTrue(source_files)
        self.assertFalse(any(path.is_symlink() for path in SKILL_ROOT.rglob("*")))

        with tempfile.TemporaryDirectory(prefix="kernelbender-codex-home-") as temporary:
            codex_home = Path(temporary) / "codex-home"
            installed = codex_home / "skills" / "kernelbender"
            installed.parent.mkdir(parents=True)
            shutil.copytree(SKILL_ROOT, installed)

            installed_files = {
                path.relative_to(installed).as_posix()
                for path in installed.rglob("*")
                if path.is_file()
            }
            self.assertEqual(source_files, installed_files)
            self.assertEqual("kernelbender", _frontmatter(installed / "SKILL.md").get("name"))
            self.assertFalse(any(part in {"evaluation", "tests", "planning"}
                                 for path in installed.rglob("*")
                                 for part in path.relative_to(installed).parts))


if __name__ == "__main__":
    unittest.main()
