"""
Create Forms for Autopsy Web App

Classes:
    - LoginForm(FlaskForm)
    - ProfileForm(FlaskForm)
    - PostmortemForm(FlaskForm)
    - SupportForm(FlaskForm)
    - SearchForm(FlaskForm)
    - RequestResetForm(FlaskForm)
    - ResetForm(FlaskForm)
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     TextAreaField, HiddenField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf
from wtforms.validators import ValidationError
from autopsy_app.model import User


class RegistrationForm(FlaskForm):
    """
    Represents RegistrationForm

    Attributes:
        name : StringField
            User name
        email : StringField
            User's email, must be uniq
        password : PasswordField
            User's password, min=3,max=20 length
        confirm_password : PasswordField
            Password confirmation, must be equal to password
    """
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=3, max=20),
                                                 EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        """
        Validates User's email
        """
        email = User.query.filter_by(user_email=email.data).first()
        if email:
            msg = "Account is already exist, see below to reset your password"
            raise ValidationError(msg)


class LoginForm(FlaskForm):
    """
    Represents LoginForm

    Attributes:
        email : StringField
            User's email, must be uniq
        password : PasswordField
            User's password, min=3,max=20 length
        remember : BooleanField
            Used by flask-login to store session over the time
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class ProfileForm(FlaskForm):
    """
    Represents ProfileForm

    Attrrbutes:
        name : StringField
            User name
        password : PasswordField
            User's password, min=3,max=20 length
        confirm_password : PasswordField
            Password confirmation, must be equal to password
        avatar : HiddenField
            Hidden field to have capability to change avatar from collection
    """
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=3, max=20),
                                                 EqualTo('password')])
    avatar = HiddenField('Avatar')
    submit = SubmitField('Update Profile')


class PostmortemForm(FlaskForm):
    """
    Represents  PostmortemForm

    Attrrbutes:
        title : StringField
            Postmortem' title
        impact : SelectField
            The value of impact
        mortem : TextAreaField
            Postmortem body
        resolution : TextAreaField
            An algoruthm to suppress the issue
    """
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    impact = SelectField('Impact',
                         choices=(['minor', 'significant', 'critical']),
                         validators=[DataRequired(),
                                     AnyOf(['minor', 'significant',
                                           'critical'], 'Wrong Impact')])
    mortem = TextAreaField('Mortem details', validators=[DataRequired()])
    resolution = TextAreaField('Mortem resolution')
    submit = SubmitField('Postmortem!')


class SupportForm(FlaskForm):
    """
    Represents  SupportForm

    Attrrbutes:
        subject : StringField
            Postmortem' title
        content : TextAreaField
            Case body
        attach : FileField
            Screenshot attachment
    """
    subject = StringField('Subject', validators=[DataRequired(),
                                                 Length(max=100)])
    content = TextAreaField('Case details',
                            validators=[DataRequired()])
    attach = FileField('Attach a screenshot',
                       validators=[FileAllowed(['jpg', 'png'],
                                               'Images only!')])
    submit = SubmitField('Request for help')


class SearchForm(FlaskForm):
    """
    Represents  SearchForm

    Attrrbutes:
        title : StringField
            Search request
    """
    title = StringField('Type to search', validators=[DataRequired(),
                                                      Length(max=100)])
    submit = SubmitField('help')


class RequestResetForm(FlaskForm):
    """
    Represents  RequestResetForm

    Attrrbutes:
        email : StringField
            User's email for request reseting a password
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Generate reset URL')


class ResetForm(FlaskForm):
    """
    Represents ResetForm

    Attrrbutes:
        password : PasswordField
            User's new password, min=3,max=20 length
        confirm_password : PasswordField
            New Password confirmation, must be equal to password
    """
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=3, max=20),
                                                 EqualTo('password')])
    submit = SubmitField('Update Password')
