from flask_mail import Message
from app import mail

def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
# Compare this snippet from backend/app/utils/utils.py:
# #backend/app/utils/utils.py
#
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)
# Compare this snippet from backend/app/models.py:
from app import db
from datetime import datetime

