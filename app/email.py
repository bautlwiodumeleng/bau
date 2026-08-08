from py_compile import main
import secrets

from flask_mail import Message
from app import mail
from datetime import datetime, timedelta
import secrets
from app import db

def send_reset_email(user):

    print("Inside send_reset_email()")
       
    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

    
    db.session.commit()

    print("Token:", token)

    msg = Message(
        "Password Reset Request",
        recipients=[user.email]
    )

    msg.body = f"""
    Hello {user.username},

    Click the link below:

    http://127.0.0.1:5000/reset_password/{token}
    """

    print("About to call mail.send()")

    mail.send(msg)

    print("mail.send() completed")