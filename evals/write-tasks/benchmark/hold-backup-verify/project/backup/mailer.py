"""Send mail."""

import smtplib
from email.message import EmailMessage


def send(to, subject, body, smtp=None):
    """Send one message. smtp is an open SMTP connection; without one, localhost is used."""
    message = EmailMessage()
    message["To"] = to
    message["From"] = "nas@localhost"
    message["Subject"] = subject
    message.set_content(body)
    connection = smtp or smtplib.SMTP("localhost")
    connection.send_message(message)
    if smtp is None:
        connection.quit()
