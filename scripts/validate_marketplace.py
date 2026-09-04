#!/usr/bin/env python3
"""Validate the public marketplace without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "got-skill"
SKILLS = PLUGIN / "skills"
FORBIDDEN_EXTENSIONS = {".doc", ".docx", ".pdf", ".xml"}
FORBIDDEN_TERMS = ("finaxys",)


def validate_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return {}


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    manifest = skill_dir / "SKILL.md"
    if not manifest.is_file():
        errors.append(f"Missing {manifest.relative_to(ROOT)}")
        return
    text = manifest.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        errors.append(f"Missing frontmatter in {manifest.relative_to(ROOT)}")
        return
    frontmatter = match.group(1)
    if not re.search(rf"^name:\s*{re.escape(skill_dir.name)}\s*$", frontmatter, re.MULTILINE):
        errors.append(f"Wrong name in {manifest.relative_to(ROOT)}")
    if not re.search(r"^description:\s*.+", frontmatter, re.MULTILINE):
        errors.append(f"Missing description in {manifest.relative_to(ROOT)}")
    if "TODO" in text:
        errors.append(f"Unfinished TODO in {manifest.relative_to(ROOT)}")
    references = skill_dir / "references"
    if references.exists():
        for path in references.rglob("*"):
            if path.is_file() and path.suffix.lower() != ".md":
                errors.append(f"Non-Markdown reference: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    marketplace = validate_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    plugin = validate_json(PLUGIN / ".claude-plugin" / "plugin.json", errors)
    codex_plugin = validate_json(PLUGIN / ".codex-plugin" / "plugin.json", errors)
    codex_marketplace = validate_json(ROOT / ".agents" / "plugins" / "marketplace.json", errors)
    entries = marketplace.get("plugins", [])
    if not entries or entries[0].get("source") != "./plugins/got-skill":
        errors.append("Marketplace source must target ./plugins/got-skill")
    if plugin.get("name") != "got-skill":
        errors.append("Plugin name must be got-skill")
    if codex_plugin.get("name") != "got-skill":
        errors.append("Codex plugin name must be got-skill")
    codex_entries = codex_marketplace.get("plugins", [])
    if not codex_entries or codex_entries[0].get("source", {}).get("path") != "./plugins/got-skill":
        errors.append("Codex marketplace source must target ./plugins/got-skill")
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)
    public_roots = {"plugins", ".claude-plugin", ".agents", ".github", "scripts"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] not in public_roots:
            continue
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            errors.append(f"Forbidden source file: {relative}")
        try:
            text = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for term in FORBIDDEN_TERMS:
            if term in text and path.name not in {"validate_marketplace.py"}:
                errors.append(f"Forbidden term in {relative}: {term}")
    if errors:
        print("Marketplace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Marketplace valid: {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
