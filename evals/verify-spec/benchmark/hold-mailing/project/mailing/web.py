"""The public pages. A page takes the service and the part of the path after its prefix, and returns (status, text)."""

from mailing.addresses import InvalidAddress
from mailing.service import AlreadySubscribed
from mailing.tokens import BadToken, read


def subscribe_page(service, address):
    try:
        service.subscribe(address)
    except InvalidAddress:
        return 400, "That is not an email address."
    except AlreadySubscribed:
        return 409, "That address is already on the list."
    return 200, "Check your mail to confirm."


def confirm_page(service, token):
    try:
        service.confirm(token)
    except (BadToken, KeyError):
        return 404, "That link is not valid."
    return 200, "You are subscribed."


def unsubscribe_page(service, token):
    try:
        service.unsubscribe(read(token))
    except (BadToken, KeyError):
        return 404, "That link is not valid."
    return 200, "You are unsubscribed."


ROUTES = {
    "/subscribe/": subscribe_page,
    "/confirm/": confirm_page,
}


def handle(service, path):
    for prefix, page in ROUTES.items():
        if path.startswith(prefix):
            return page(service, path[len(prefix):])
    return 404, "Not found."
