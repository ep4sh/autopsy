"""
Add  mail capabilities for Autopsy Web App

Methods:
    def send_admin_email(db, support_case) -> None
    def send_email(email, token) -> None
"""
from flask import url_for
from flask_mail import Message
from autopsy_app import app, mail
from autopsy_app.model import User, UserRoles


def send_admin_email(db_obj, support_case):
    """
    Send announcement for each member of 'admin' groups
    When the support case is being created
    """
    msg = Message('Autopsy Web app: a support case has been created')
    msg.sender = app.config['MAIL_USERNAME']
    email_dl = db_obj.session.query(
                                UserRoles.role_id,
                                User.user_email).filter(
                                UserRoles.role_id == 1).join(User).all()
    case_author = User.query.filter(User.id==support_case.user_id).first()
    admin_dl = [mail[1] for mail in email_dl]
    msg.recipients = admin_dl
    msg.body = f"""
    Autopsy Web App: new support has been created!
    A new support case has been opened by {case_author.user_name}
    Date: {support_case.support_created}
    Subject: {support_case.support_subject}
    Content: {support_case.support_content}

    ----
    This is an auto-generated message, please don't reply.

    """
    mail.send(msg)


def send_email(email, token):
    """
    Create an email request for password reset procedure
    """
    msg = Message('Password Reset for Autopsy')
    msg.sender = app.config['MAIL_USERNAME']
    msg.recipients = [email]
    msg.body = f"""
    Good mortem! How is it going?

    To reset your password, please click on the following link:
    {url_for('reset_password', token=token, _external=True)}

    If you didn't request this request - be beware of the Great Evil!
    """
    mail.send(msg)
