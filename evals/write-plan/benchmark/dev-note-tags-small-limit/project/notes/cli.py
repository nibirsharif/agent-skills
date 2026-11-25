"""The command line: add <text>, list."""

import argparse

from notes.store import Store


def main(argv, out, path="notes.json"):
    parser = argparse.ArgumentParser(prog="notes")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("add").add_argument("text")
    commands.add_parser("list")
    args = parser.parse_args(argv)
    store = Store(path)
    if args.command == "add":
        note = store.add(args.text)
        print(f"Added note {note['id']}", file=out)
        return 0
    for note in store.load():
        print(f"{note['id']}  {note['text']}", file=out)
    return 0
