import smtplib
from email.mime.text import MIMEText

SENDER = "your_email@gmail.com"
PASSWORD = "your_app_password"

def send_email(receiver, subject, message):

    msg = MIMEText(message)

    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(SENDER, PASSWORD)

    server.sendmail(SENDER, receiver, msg.as_string())

    server.quit()