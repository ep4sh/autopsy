import sys
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET")
app.mail_username = os.getenv("MAIL_USERNAME")
app.mail_password = os.getenv("MAIL_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autopsy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = app.mail_username
app.config['MAIL_PASSWORD'] = app.mail_password

mail = Mail(app)
flask_bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from autopsy_app import routes
