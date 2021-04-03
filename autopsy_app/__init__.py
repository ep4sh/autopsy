import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
load_dotenv()

# securty settings
app.secret_key = os.getenv("FLASK_SECRET")
# mail settings
app.mail_server = os.getenv("MAIL_SERVER")
app.mail_port = os.getenv("MAIL_PORT")
app.mail_use_ssl = os.getenv("MAIL_USE_SSL")
app.mail_username = os.getenv("MAIL_USERNAME")
app.mail_password = os.getenv("MAIL_PASSWORD")
# database settings
app.db_host = os.getenv("DATABASE_HOST")
app.db_user = os.getenv("DATABASE_USER")
app.db_password = os.getenv("DATABASE_PASSWORD")
app.db_port = os.getenv("DATABASE_PORT")
app.db_name = os.getenv("DATABASE_NAME")
app.db_uri = (f"postgresql://{app.db_user}:{app.db_password}@"
              f"{app.db_host}:{app.db_port}/{app.db_name}")
app.db_track_modifications = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

# Flask config
app.config['SQLALCHEMY_DATABASE_URI'] = app.db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.db_track_modifications

app.config['MAIL_SERVER'] = app.mail_server
app.config['MAIL_PORT'] = app.mail_port
app.config['MAIL_USE_SSL'] = app.mail_use_ssl
app.config['MAIL_USERNAME'] = app.mail_username
app.config['MAIL_PASSWORD'] = app.mail_password

mail = Mail(app)
flask_bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from autopsy_app import routes
