#!/usr/bin/env python3
"""Checks that apply to every skill under skills/ and examples/, and to the plugin manifest."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOTS = [ROOT / "skills", ROOT / "examples"]

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
ALLOWED_FIELDS = {"name", "description", "disable-model-invocation"}
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Return the top-level frontmatter fields, or None when there is no frontmatter.

    Handles quoted values, plain values wrapped onto indented lines, and `|` / `>`
    block values, so a long description is measured in full.
    """
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.DOTALL)
    if not m:
        return None
    fields, key, joiner = {}, None, " "
    for line in m.group(1).splitlines():
        if key and (line.startswith((" ", "\t")) or not line.strip()):
            part = line.strip()
            if part:
                fields[key] = f"{fields[key]}{joiner}{part}" if fields[key] else part
            continue
        k, sep, v = line.partition(":")
        if not sep or line.startswith((" ", "\t", "#")):
            key = None
            continue
        key, v = k.strip(), v.strip()
        if v[:1] in ("|", ">"):
            fields[key], joiner = "", "\n" if v[0] == "|" else " "
        else:
            fields[key], joiner = unquote(v), " "
    return fields


def unsafe_plain_fields(text):
    """Names of frontmatter fields whose unquoted value YAML parsers reject or cut short.

    In a plain (unquoted, non-block) value, `: ` starts a nested mapping and ` #` starts a comment.
    Quote the value, or rephrase it, to fix.
    """
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.DOTALL)
    values, key = {}, None
    for line in (m.group(1).splitlines() if m else []):
        if key and (line.startswith((" ", "\t")) or not line.strip()):
            values[key] += " " + line.strip()
            continue
        k, sep, v = line.partition(":")
        key = None if not sep or line.startswith((" ", "\t", "#")) else k.strip()
        if key:
            values[key] = v.strip()
    plain = {k: v for k, v in values.items() if v[:1] not in ("|", ">", '"', "'")}
    return [k for k, v in plain.items() if re.search(r": | #", v)]


def visible_markdown(text):
    """Markdown with code blocks, inline code, and HTML comments removed."""
    text = FENCE_RE.sub("", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    return INLINE_CODE_RE.sub("", text)


def check_skill(skill_dir, seen_names):
    """Return a list of problems for one skill. Records its name in seen_names."""
    label = skill_dir.relative_to(ROOT)
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{label}: missing SKILL.md"]

    fm = parse_frontmatter(skill_md.read_text())
    if fm is None:
        return [f"{label}: SKILL.md has no frontmatter"]

    name, desc = fm.get("name", ""), fm.get("description", "")

    if not name:
        errors.append(f"{label}: missing name")
    else:
        if name != skill_dir.name:
            errors.append(f"{label}: name '{name}' must match the directory name '{skill_dir.name}'")
        if not KEBAB_RE.match(name):
            errors.append(f"{label}: name '{name}' must be kebab-case (lowercase letters, digits, single hyphens)")
        if len(name) > MAX_NAME:
            errors.append(f"{label}: name is {len(name)} characters (limit {MAX_NAME})")
        key = name.lower()
        if key in seen_names:
            errors.append(f"{label}: name '{name}' is already used by {seen_names[key]}")
        else:
            seen_names[key] = label

    if not desc:
        errors.append(f"{label}: missing description")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"{label}: description is {len(desc)} characters (limit {MAX_DESCRIPTION})")

    for field in unsafe_plain_fields(skill_md.read_text()):
        errors.append(f"{label}: frontmatter `{field}` has `: ` or ` #` in an unquoted value, which YAML parsers reject; rephrase it or quote it")

    if fm.get("disable-model-invocation", "true") not in ("true", "false"):
        errors.append(f"{label}: disable-model-invocation must be true or false")

    extra = set(fm) - ALLOWED_FIELDS
    if extra:
        errors.append(f"{label}: unexpected frontmatter fields {sorted(extra)} (allowed: {sorted(ALLOWED_FIELDS)})")

    for md in sorted(skill_dir.rglob("*.md")):
        for target in LINK_RE.findall(visible_markdown(md.read_text())):
            path = (md.parent / target.split("#", 1)[0]).resolve()
            if not path.exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link '{target}'")
            elif not path.is_relative_to(skill_dir.resolve()):
                errors.append(f"{md.relative_to(ROOT)}: link '{target}' points outside the skill folder")
    return errors


def check_plugin():
    """Return a list of problems with the skills listed in .claude-plugin/plugin.json."""
    if not PLUGIN_JSON.is_file():
        return []
    label = PLUGIN_JSON.relative_to(ROOT)
    try:
        skills = json.loads(PLUGIN_JSON.read_text()).get("skills", [])
    except ValueError as e:
        return [f"{label}: not valid JSON: {e}"]
    if not isinstance(skills, list):
        return [f"{label}: skills must be a list of skill folders"]
    errors = []
    for entry in skills:
        path = (ROOT / entry).resolve()
        if path.parent != (ROOT / "skills").resolve():
            errors.append(f"{label}: skill '{entry}' must be a folder directly under skills/")
        elif not (path / "SKILL.md").is_file():
            errors.append(f"{label}: skill '{entry}' has no SKILL.md")
    return errors


def main():
    errors, count, seen_names = check_plugin(), 0, {}
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for skill_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
            count += 1
            errors += check_skill(skill_dir, seen_names)

    for e in errors:
        print(f"FAIL {e}")
    print(f"{count} skills checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
