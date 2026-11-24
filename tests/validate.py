#!/usr/bin/env python3
"""Checks that apply to every skill under skills/, and to the plugin manifest."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOTS = [ROOT / "skills"]

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
ALLOWED_FIELDS = {"name", "description", "disable-model-invocation"}
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"

# The most words each skill may make the agent read on every run, and the files that count besides SKILL.md:
# the references SKILL.md says to read on every run. A file read only in one situation (saving a file, a
# follow-up, an agent that cannot run commands) is not listed. Words are counted as `wc -w` counts them.
# write-tasks and write-plan list their file template: their runs read it for a chat reply too, which follows the
# template's order.
# Each budget is the count when it was set plus about 100 words, so a reworded rule fits and a new paragraph
# does not: cut words elsewhere, or raise the number in the same commit and say why. Lower it after a trim.
WORD_BUDGETS = {
    "build-phase": (2800, ["references/build-rules.md"]),
    "implement-task": (3350, ["references/implement-rules.md", "references/examples.md"]),
    "verify-spec": (3020, ["references/verify-rules.md", "references/examples.md"]),
    "write-plan": (3100, ["references/plan-rules.md", "references/examples.md", "references/plan-template.md"]),
    "write-spec": (4700, ["references/ears-rules.md", "references/examples.md"]),
    "write-tasks": (3330, ["references/task-rules.md", "references/examples.md", "references/tasks-template.md"]),
}


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


def check_budget(skill_dir, budgets=None):
    """Return a list of problems with the words one skill reads on every run. See WORD_BUDGETS."""
    budgets = WORD_BUDGETS if budgets is None else budgets
    label = f"skills/{skill_dir.name}"
    if not (skill_dir / "SKILL.md").is_file():
        return []  # check_skill reports it
    if skill_dir.name not in budgets:
        return [f"{label}: no word budget; add the skill to WORD_BUDGETS in tests/validate.py"]
    limit, extra = budgets[skill_dir.name]
    errors, counts = [], {}
    for name in ["SKILL.md", *extra]:
        path = (skill_dir / name).resolve()
        if not path.is_file() or not path.is_relative_to(skill_dir.resolve()):
            errors.append(f"{label}: word budget names '{name}', which is not a file in the skill folder")
        else:
            counts[name] = len(path.read_text().split())
    total = sum(counts.values())
    if not errors and total > limit:
        parts = ", ".join(f"{name} {n}" for name, n in counts.items())
        errors.append(f"{label}: {total} words read on every run, over its budget of {limit} ({parts}). "
                      "Cut words, or raise the budget in WORD_BUDGETS in tests/validate.py and say why in the commit")
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


def check_release(root=ROOT):
    """Return problems with release metadata: versions agree, the README and CHANGELOG match plugin.json."""
    plugin_json = root / ".claude-plugin" / "plugin.json"
    market_json = root / ".claude-plugin" / "marketplace.json"
    if not plugin_json.is_file():
        return []
    try:
        plugin = json.loads(plugin_json.read_text())
        market = json.loads(market_json.read_text()) if market_json.is_file() else None
    except ValueError as e:
        return [f"release metadata: not valid JSON: {e}"]
    errors, version = [], plugin.get("version", "")

    if market is not None:
        entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
        if not entries:
            errors.append(f"{market_json.relative_to(root)}: no entry for plugin '{plugin.get('name')}'")
        elif entries[0].get("version") != version:
            errors.append(f"{market_json.relative_to(root)}: version '{entries[0].get('version')}' differs from plugin.json '{version}'")

    changelog = root / "CHANGELOG.md"
    if changelog.is_file() and not re.search(rf"^## {re.escape(version)}\s*$", changelog.read_text(), re.MULTILINE):
        errors.append(f"CHANGELOG.md: no '## {version}' heading for the current plugin version")

    readme = root / "README.md"
    if readme.is_file():
        listed = {Path(s).name for s in plugin.get("skills", [])}
        in_table = set(re.findall(r"^\| \[([a-z0-9-]+)\]\(skills/", readme.read_text(), re.MULTILINE))
        for name in sorted(listed - in_table):
            errors.append(f"README.md: skill '{name}' is in plugin.json but not in the skills table")
        for name in sorted(in_table - listed):
            errors.append(f"README.md: skill '{name}' is in the skills table but not in plugin.json")
    return errors


def main():
    errors, count, seen_names, folders = check_plugin() + check_release(), 0, {}, set()
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for skill_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
            count += 1
            folders.add(skill_dir.name)
            errors += check_skill(skill_dir, seen_names)
            errors += check_budget(skill_dir)
    for name in sorted(set(WORD_BUDGETS) - folders):
        errors.append(f"tests/validate.py: WORD_BUDGETS has '{name}', which is not a skill")

    for e in errors:
        print(f"FAIL {e}")
    print(f"{count} skills checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
