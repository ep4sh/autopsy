from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError
from autopsy_app.model import User


class RegistrationForm(FlaskForm):
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
        email = User.query.filter_by(user_email=email.data).first()
        if email:
            msg = "Account is already exist, see below to reset your password"
            raise ValidationError(msg)


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=3, max=20),
                                                 EqualTo('password')])
    submit = SubmitField('Update Profile')


