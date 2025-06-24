from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from .extensions import mail

def generate_token(data, salt):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(data, salt=salt)

def verify_token(token, salt, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        return s.loads(token, salt=salt, max_age=max_age)
    except Exception as e:
        print(f"[Token Error] {e}")
        return None

from flask_mail import Message
from .extensions import mail

def send_email(subject: str, recipient: str, body: str):
    # Force string types just in case
    subject = str(subject)
    recipient = str(recipient)
    body = str(body)

    try:
        msg = Message(subject=subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print(f"[Email Error] {e}")
