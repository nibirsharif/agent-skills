#!/usr/bin/env python3
"""Find the requirements.md that verify-spec works from, or say what to reply when there is none.

Usage: python3 find_requirements.py [--feature NAME | --path PATH] [--root DIR]

Run it with the project as the current directory. --root is the project root; without it, the git
repository's root, or the current directory outside a repository. Prints one of these and exits 0:

  found <path>   the file to use
  stop <line>    <line> is the whole reply: the no-requirements-file stop line
  ask <what>     ask the user <what>

--feature NAME looks at <spec_output_dir>/NAME/requirements.md and nowhere else: another feature's requirements is
never the answer. --path PATH looks at PATH. With neither, the one <spec_output_dir>/*/requirements.md is used;
several, or none, is a question. spec_output_dir comes from .agent-skills-config.yaml in the project
root, else from ~/.agent-skills-config.yaml.

Exits 2 on a usage error. Python 3 standard library only.
"""

FILE = "requirements.md"
STOP = "No requirements file found at {path}. Run write-spec first, then run verify-spec again."
BESIDE = []  # (file that must be beside it, stop line when it is not)
SUMMARY = ""  # the lines before `Stopped:` when the reply is a summary
SETTINGS = []  # (config key, the word it is printed under after `found`, default)

# Everything below this line is the same in every skill's copy of this script (tests/test_find_scripts.py checks it):
# a skill cannot load code from another skill's folder.

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG = ".agent-skills-config.yaml"


def git(root, *args):
    """A git command's output, or "" when it fails or git is missing."""
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    except OSError:
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def project_root(start):
    """The git repository's root, or start outside a repository."""
    top = git(start, "rev-parse", "--show-toplevel")
    return Path(top) if top else start


def config_value(path, key):
    """The value of a top-level `key: value` line in a YAML file, or "" when the file or the value is missing."""
    try:
        text = path.read_text()
    except OSError:
        return ""
    for line in text.splitlines():
        m = re.match(rf"{re.escape(key)}:(.*)$", line)
        if m:
            value = m.group(1).strip()
            if value[:1] in "\"'" and value[-1:] == value[:1] and len(value) > 1:
                return value[1:-1]
            return re.sub(r"\s+#.*$", "", value).strip() if not value.startswith("#") else ""
    return ""


def spec_output_dir(root, home):
    """The configured value as written (so a relative one stays relative in a reply), or ""."""
    return config_value(root / CONFIG, "spec_output_dir") or config_value(home / CONFIG, "spec_output_dir")


def stop(root, feature, line):
    """What to print for a stop: the line, or the whole stopped summary for a skill whose reply is one."""
    if not SUMMARY:
        return "stop " + line
    branch = git(root, "branch", "--show-current") or "none"
    return "\n".join(["stop", SUMMARY.format(feature=feature, branch=branch), "Stopped: " + line])


def found(root, home, shown):
    """A file was found at the shown path: check the files that must be beside it, then read the settings."""
    folder = str(Path(shown).parent)
    for name, line in BESIDE:
        beside = f"{folder}/{name}"
        if not (root / Path(beside).expanduser()).is_file():
            return stop(root, Path(folder).name, line.format(path=beside))
    lines = [f"found {shown}"]
    for key, word, default in SETTINGS:
        value = config_value(root / CONFIG, key) or config_value(home / CONFIG, key)
        if value and not value.isdigit():
            return f"ask {key} in {CONFIG} is {value}, not a whole number: the number to use"
        lines.append(f"{word} {int(value) if value else default}")
    return "\n".join(lines)


def find(root, home, feature=None, path=None):
    """The text to print."""
    if path:
        if (root / Path(path).expanduser()).is_file():
            return found(root, home, path)
        return stop(root, Path(path).parent.name or "?", STOP.format(path=path))
    spec = spec_output_dir(root, home)
    if not spec:
        return f"ask No spec_output_dir is set and no path was given: the path of {FILE}"
    base = root / Path(spec).expanduser()
    shown = spec.rstrip("/")
    if feature:
        wanted = f"{shown}/{feature}/{FILE}"
        if (base / feature / FILE).is_file():
            return found(root, home, wanted)
        return stop(root, feature, STOP.format(path=wanted))
    names = sorted(p.parent.name for p in base.glob(f"*/{FILE}") if p.is_file())
    if len(names) == 1:
        return found(root, home, f"{shown}/{names[0]}/{FILE}")
    if names:
        return "ask Which feature: " + ", ".join(names)
    return f"ask No {FILE} under {shown} and no feature was named: which feature, or the path of {FILE}"


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip().removeprefix("Usage: "))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--feature")
    group.add_argument("--path")
    parser.add_argument("--root")
    args = parser.parse_args(argv)
    if args.feature is not None and (not args.feature.strip() or "/" in args.feature or args.feature in (".", "..")):
        parser.error("--feature is a folder name, without a slash")
    root = Path(args.root).resolve() if args.root else project_root(Path.cwd())
    print(find(root, Path.home(), args.feature, args.path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
