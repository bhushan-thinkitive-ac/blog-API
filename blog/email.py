import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


def send_password_reset_email(to_email: str, reset_code: str):
    # SMTP server configuration
    smtp_server= 'smtp.gmail.com' 
    smtp_port = 587
    smtp_username = 'your_email' 
    smtp_password = 'your_password'  

    # Email content
    from_email = 'bhushan.chaudhari@thinkitive.com'
    subject = 'Password Reset Request'
    body = f"""
    Hi,

    We received a request to reset your password. Please use the following code to reset your password:

    Reset Code: {reset_code}

    If you did not request a password reset, please ignore this email.

    Best regards,
    Your Company
    """

    # Construct the email message
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Thinkitive Technologies', from_email))
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() 
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            print('Password reset email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')



























# from mailgun import Mailgun
# import requests
# from . config import api_key, domain


# def send_password_reset_email(to_email: str, reset_code: str):
#     #Mailgun config

    
    
#     # Mailgun API endpoint
#     url = f'https://api.mailgun.net/v3/{domain}/messages'
    
#     # Email content
#     from_email = 'bhushan.chaudhari@thinkitive.com'
#     subject = 'Password Reset Request'
#     body = f"""
#     Hi,

#     We received a request to reset your password. Please use the following code to reset your password:

#     Reset Code: {reset_code}

#     If you did not request a password reset, please ignore this email.

#     Best regards,
#     Your Company
#     """

#     # Send the email using Mailgun API
#     response = requests.post(
#         url,
#         auth=('api', api_key),
#         data={
#             'from': from_email,
#             'to': to_email,
#             'subject': subject,
#             'text': body
#         }
#     )

#     # Check the response
#     if response.status_code == 200:
#         print('Password reset email sent successfully.')
#     else:
#         print(f'Error sending email: {response.status_code} - {response.text}')

# # # Example usage
# # send_password_reset_email('recipient@example.com', '123456')
