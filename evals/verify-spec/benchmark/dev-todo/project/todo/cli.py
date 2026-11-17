"""The command line: add <title> [--due DATE], list [--overdue]."""

import argparse
import datetime

from todo import tasks as store


def main(argv, tasks, out, today=None):
    parser = argparse.ArgumentParser(prog="todo")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    add.add_argument("--due")
    show = commands.add_parser("list")
    show.add_argument("--overdue", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "add":
        due = None
        if args.due is not None:
            due = store.parse_due(args.due)
            if due is None:
                print(f"Invalid date: {args.due}", file=out)
                return 1
        store.add(tasks, args.title, due)
        return 0

    today = today or datetime.date.today()
    shown = store.overdue(tasks, today) if args.overdue else store.listing(tasks)
    for task in shown:
        print(f"{task['due'] or '-'}  {task['title']}", file=out)
    return 0
