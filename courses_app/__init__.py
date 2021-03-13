import os
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = ' '.join(map(bin, bytearray(os.getenv("FLASK_SECRET").encode('utf-8'))))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cnest.db'
bcrypt = Bcrypt(app)

from courses_app import routes
