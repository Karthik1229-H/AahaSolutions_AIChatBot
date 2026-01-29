import smtplib
from email.message import EmailMessage

def send_email(name, email, phone, message):
    msg = EmailMessage()
    msg["Subject"] = "AAHA AI Assistant – New Request"
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = "aahasolutions121@gmail.com"

    msg.set_content(f"""
Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("omsiva.karthik.2002@gmail.com", "nggn kima jkmp rzni")
        smtp.send_message(msg)
