"""Pages to whoever is on call. A page is for what cannot wait for mail."""


class Pager:
    def __init__(self):
        self.pages = []

    def page(self, user, message):
        self.pages.append((user.email, message))
