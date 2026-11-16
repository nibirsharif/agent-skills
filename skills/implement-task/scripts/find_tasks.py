#!/usr/bin/env python3
"""Find the tasks.md that implement-task works from, or say what to reply when there is none.

Usage: python3 find_tasks.py [--feature NAME | --path PATH] [--root DIR]

Run it from the project. --root is the project root; without it, the git repository's root, or the
current directory outside a repository. Prints one line and exits 0:

  found <path>   the file to use
  stop <line>    <line> is the whole reply: the no-tasks-file stop line
  ask <what>     ask the user <what>

--feature NAME looks at <spec_output_dir>/NAME/tasks.md and nowhere else: another feature's task list is
never the answer. --path PATH looks at PATH. With neither, the one <spec_output_dir>/*/tasks.md is used;
several, or none, is a question. spec_output_dir comes from .agent-skills-config.yaml in the project root,
else from ~/.agent-skills-config.yaml.

Exits 2 on a usage error. Python 3 standard library only.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG = ".agent-skills-config.yaml"
STOP = "No tasks file found at {path}. Run write-tasks first, then run implement-task again."


def project_root(start):
    """The git repository's root, or start outside a repository."""
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start, capture_output=True, text=True)
    except OSError:
        return start
    return Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else start


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


def find(root, home, feature=None, path=None):
    """The one line to print."""
    if path:
        return f"found {path}" if (root / Path(path).expanduser()).is_file() else "stop " + STOP.format(path=path)
    spec = spec_output_dir(root, home)
    if not spec:
        return "ask No spec_output_dir is set and no path was given: the path of tasks.md"
    base = root / Path(spec).expanduser()
    shown = spec.rstrip("/")
    if feature:
        wanted = f"{shown}/{feature}/tasks.md"
        return f"found {wanted}" if (base / feature / "tasks.md").is_file() else "stop " + STOP.format(path=wanted)
    names = sorted(p.parent.name for p in base.glob("*/tasks.md") if p.is_file())
    if len(names) == 1:
        return f"found {shown}/{names[0]}/tasks.md"
    if names:
        return "ask Which feature: " + ", ".join(names)
    return f"ask No tasks.md under {shown} and no feature was named: which feature, or the path of tasks.md"


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip())
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
