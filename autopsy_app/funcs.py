import sys
import string
import random
from flask_mail import Message
from flask import url_for

from autopsy_app import app, flask_bcrypt, mail
from autopsy_app.model import Mortem


def define_mortem_url():
    url = "".join([random.choice(string.ascii_letters) for c in range(15)])
    existing_url = Mortem.query.filter_by(mortem_url=url).first()
    return define_mortem_url() if existing_url else url


def choose_random_mortem(max_id):
    return random.randrange(1, max_id+1) if max_id else None


def send_email(rec, message):
    print(f'{rec} : {message}', file=sys.stderr)


def generate_password(data):
    return flask_bcrypt.generate_password_hash(data).decode('utf-8')


def verify_password(true_pass, data):
    return True if flask_bcrypt.check_password_hash(true_pass, data) else False


def send_email(email, token):
    msg = Message('Password Reset for Autopsy')
    msg.sender = app.config['MAIL_USERNAME']
    msg.recipients=[email]
    msg.body = f"""
    Good mortem! How is it going?

    To reset your password, please click on the following link:
    {url_for('reset_password', token=token, _external=True)}

    If you didn't request this request - be beware of the Great Evil!
    """
    mail.send(msg)
