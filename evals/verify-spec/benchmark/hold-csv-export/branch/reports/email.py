"""Mail a finished report."""

from email.message import EmailMessage


def message(to, subject, csv_text):
    mail = EmailMessage()
    mail["To"] = to
    mail["Subject"] = subject
    mail.set_content("The report is attached.")
    mail.add_attachment(csv_text.encode(), maintype="text", subtype="csv", filename="report.csv")
    return mail
