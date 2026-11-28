#!/usr/bin/env python3
"""Find the folder write-spec saves under, or say what to reply when none is set.

Usage: python3 target.py [--root DIR]

Run it with the project as the current directory. --root is the project root; without it, the git
repository's root, or the current directory outside a repository. Prints one of these and exits 0:

  dir <path>      spec_output_dir, from .agent-skills-config.yaml in the project root, else from
                  ~/.agent-skills-config.yaml. A relative one is resolved against the project root.
                  The path is printed relative to the current directory when it is inside it, so
                  that a reply can state it as the user knows it, and in full otherwise.
  ask <question>  no spec_output_dir is set: <question> is the whole reply

Exits 2 on a usage error. Python 3 standard library only.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG = ".agent-skills-config.yaml"
ASK = f'Where should I save the requirements? Give a path, set `spec_output_dir` in `{CONFIG}`, or say "chat only".'


def project_root(start):
    """The git repository's root, or start outside a repository or without git."""
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


def target(root, home, cwd):
    """The text to print."""
    spec = config_value(root / CONFIG, "spec_output_dir") or config_value(home / CONFIG, "spec_output_dir")
    if not spec:
        return "ask " + ASK
    path = (root / Path(spec).expanduser()).resolve()
    try:
        shown = path.relative_to(cwd)
    except ValueError:
        shown = path
    return f"dir {shown}"


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip().removeprefix("Usage: "))
    parser.add_argument("--root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else project_root(Path.cwd())
    print(target(root, Path.home(), Path.cwd().resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
