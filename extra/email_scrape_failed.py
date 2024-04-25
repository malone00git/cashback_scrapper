import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to send email
def send_email():
    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')
    sender_email = email
    receiver_email = email
    password = password

    # Create the email head (sender, receiver, and subject)
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email
    email["Subject"] = "Alert: status code is not 200"

    # Email body
    message = "The status code returned is not 200."
    email.attach(MIMEText(message, "plain"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.starttls()  # Secure the connection
        smtp.login(sender_email, password)  # Log in to the email account
        smtp.send_message(email)  # Send the email
