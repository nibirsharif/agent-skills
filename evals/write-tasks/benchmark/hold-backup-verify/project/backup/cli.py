"""The command line: create <source> <target>."""

import argparse

from backup.archive import write_archive


def main(argv, out):
    parser = argparse.ArgumentParser(prog="backup")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("source")
    create.add_argument("target")
    args = parser.parse_args(argv)
    print(f"Wrote {write_archive(args.source, args.target)}", file=out)
    return 0
