import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = ' '.join(map(bin, bytearray(os.getenv("FLASK_SECRET").encode('utf-8'))))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cnest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

flask_bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from courses_app import routes
