from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, HiddenField
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
    avatar = HiddenField('Avatar')
    submit = SubmitField('Update Profile')


class PostmortemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    mortem = TextAreaField('Mortem details', validators=[DataRequired()])
    submit = SubmitField('Postmortem!')


class SupportForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired(),
                                                 Length(max=100)])
    content = TextAreaField('Case details',
                            validators=[DataRequired()])
    attach = FileField('Attach a screenshot',
                       validators=[FileAllowed(['jpg', 'png'],
                                               'Images only!')])
    submit = SubmitField('Request for help')


class SearchForm(FlaskForm):
    title = StringField('Type to search', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('help')
