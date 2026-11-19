#!/usr/bin/env python3
"""Print build-phase's summary: the whole reply that ends a run.

Usage: python3 summary.py --feature NAME --phase N --branch BRANCH --implemented K --reworked R
                          --verify VALUE [--check-by-hand "ID: check" ...]
                          (--stopped REASON | --title PHASE_TITLE)

--verify is what follows `Verify: `: the tally, `not run`, or `no usable report`. --check-by-hand is
given once per manual check row, in the report's order. --stopped makes the run stopped, with REASON
on the `Stopped:` line; --title makes it done, with PHASE_TITLE in the `Next:` line.

Prints the summary lines and exits 0. They are the whole reply, copied as printed. Exits 2 on a usage
error, such as a value with a line break or both --stopped and --title. Python 3 standard library only.
"""

import argparse
import sys


def summary(feature, phase, branch, implemented, reworked, verify, checks=(), stopped=None, title=None):
    """The summary lines, joined. Exactly one of stopped and title is given."""
    lines = [
        f"Phase {phase} of {feature}: {'stopped' if stopped else 'done'}",
        f"Branch: {branch}",
        f"Tasks: {implemented} implemented, {reworked} reworked",
        f"Verify: {verify}",
    ]
    lines += [f"Check by hand: {check}" for check in checks]
    if stopped:
        lines.append(f"Stopped: {stopped}")
    else:
        lines.append(f'Next: push {branch}, open a PR titled "{feature} phase {phase}: {title}", and run /code-review')
    return "\n".join(lines)


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1].strip().removeprefix("Usage: "))
    parser.add_argument("--feature", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--implemented", required=True, type=int)
    parser.add_argument("--reworked", required=True, type=int)
    parser.add_argument("--verify", required=True)
    parser.add_argument("--check-by-hand", action="append", default=[], dest="checks")
    end = parser.add_mutually_exclusive_group(required=True)
    end.add_argument("--stopped")
    end.add_argument("--title")
    args = parser.parse_args(argv)
    values = [args.feature, args.phase, args.branch, args.verify, args.stopped or args.title, *args.checks]
    if any(not v.strip() or "\n" in v for v in values):
        parser.error("every value is one non-empty line")
    if args.implemented < 0 or args.reworked < 0:
        parser.error("--implemented and --reworked are counts, 0 or more")
    for prefix, value in [("Stopped: ", args.stopped), ("Verify: ", args.verify)]:
        if value and value.startswith(prefix):
            parser.error(f"give the value without the {prefix.strip()} label: the script writes it")
    print(summary(args.feature, args.phase, args.branch, args.implemented, args.reworked, args.verify,
                  args.checks, args.stopped, args.title))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
