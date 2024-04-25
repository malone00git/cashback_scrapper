import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

file_name = ''
error_code = ''


# Takes in file name and response error code from the scrape file that failed to scrape a website
def curr_file_and_err_code(name, code):
    global file_name
    global error_code
    file_name = name
    error_code = code


# Function to send email with file_name and response error code
def send_email():
    global file_name
    global error_code
    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')
    print(email, password)
    sender_email = email
    receiver_email = email
    password = password

    # Create the email head (sender, receiver, and subject)
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = receiver_email
    email['Subject'] = 'Alert: status code is not 200'

    # Email body
    message = 'File name: ' + file_name + '\n'
    message += 'Error code: ' + error_code + '\n'
    email.attach(MIMEText(message, 'plain'))

    # Connect to Gmail's SMTP server
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Log in to the email account
            server.send_message(email)  # Send the email
    except smtplib.SMTPException as e:
        print(f'Failed to send email: {e}')


send_email()
