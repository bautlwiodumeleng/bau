from flask_mail import Message
from app import mail

def send_reset_email(user):

    print("Inside send_reset_email()")

    token = user.get_reset_token()

    print("Token:", token)

    msg = Message(
        "Password Reset Request",
        recipients=[user.email]
    )

    msg.body = f"""
Hello {user.username},

Click the link below to reset your password:

http://127.0.0.1:5000/reset_password/{token}

If you did not request a password reset, you can ignore this email.

"""

    print("About to call mail.send()")

    mail.send(msg)

    print("mail.send() completed")

