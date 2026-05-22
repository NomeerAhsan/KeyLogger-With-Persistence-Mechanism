import smtplib
from email.message import EmailMessage
import os

username = os.getlogin()

def send_file_email(
    sender_email="your sender mail",
    sender_password="app password",
    receiver_email="mail to receive",
    subject="Test File",
    body="Here is the file.",
    file_path=fr"path to your file"
):
    # Create email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    # Read and attach file
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = file_path.split("\\")[-1]

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=file_name
    )

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    print("File sent successfully.")

send_file_email()


