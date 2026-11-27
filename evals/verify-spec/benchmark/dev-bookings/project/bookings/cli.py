"""The command line: book <room> <email> <start> <hours> <price> <payment>, list <room>."""

import argparse
import datetime
import decimal

from bookings.service import RefundFailed, RoomTaken


def book_command(args, service, out):
    start = datetime.datetime.fromisoformat(args.start)
    end = start + datetime.timedelta(hours=args.hours)
    try:
        booking = service.book(args.room, args.email, start, end, decimal.Decimal(args.price), args.payment)
    except RoomTaken:
        print(f"{args.room} is taken at that time.", file=out)
        return 1
    print(f"Booked {args.room}: booking {booking.id}.", file=out)
    return 0


def list_command(args, service, out):
    for booking in service.store.for_room(args.room):
        print(f"{booking.id}  {booking.start:%Y-%m-%d %H:%M}  {booking.user_email}", file=out)
    return 0


def cancel_command(args, service, out):
    try:
        refund = service.cancel(args.id)
    except RefundFailed as error:
        print(f"Not cancelled: {error}", file=out)
        return 1
    print(f"Cancelled booking {args.id}. Refunded {refund:.2f}.", file=out)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="bookings")
    commands = parser.add_subparsers(dest="command", required=True)
    book = commands.add_parser("book")
    for name in ("room", "email", "start"):
        book.add_argument(name)
    book.add_argument("hours", type=int)
    book.add_argument("price")
    book.add_argument("payment")
    book.set_defaults(run=book_command)
    show = commands.add_parser("list")
    show.add_argument("room")
    show.set_defaults(run=list_command)
    return parser


def main(argv, service, out):
    args = build_parser().parse_args(argv)
    return args.run(args, service, out)
