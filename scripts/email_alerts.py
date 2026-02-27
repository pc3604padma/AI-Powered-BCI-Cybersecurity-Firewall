import smtplib
from email.mime.text import MIMEText

SENDER = "uropbcd24@gmail.com"
PASSWORD = "gwhr scse fntz foni"
RECEIVER = "padmanathanchinnathurai24@gmail.com"

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
