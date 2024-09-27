from flask_mail import Message
from .mail import mail  # Import the mail object from mail.py

def send_custom_email(recipient_email, subject, body):
    """
    Function to send an email with a custom subject and body.
    
    :param recipient_email: The email address of the recipient
    :param subject: The subject of the email
    :param body: The body content of the email
    """
    try:
        msg = Message(subject,
                      recipients=[recipient_email])  # Setting the recipient and subject
        msg.body = body  # Setting the body content
        mail.send(msg)  # Sending the email
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
