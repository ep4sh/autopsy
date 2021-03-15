from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import ValidationError
from autopsy_app.model import User


class RegistrationForm(FlaskForm):
    # Email == Username
    username = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(),
                                                  Length(min=3, max=20),
                                                  EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            msg = "Username is already taken.."
            raise ValidationError(msg)

class LoginForm(FlaskForm):
    username = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                           validators=[DataRequired(), Length(min=3, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
