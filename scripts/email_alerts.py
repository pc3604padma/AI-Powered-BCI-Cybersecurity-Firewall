import smtplib
from email.mime.text import MIMEText

SENDER = "your_email@gmail.com"
PASSWORD = "your_app_password"
RECEIVER = "receiver_email@gmail.com"

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)