import os
from flask import Flask

app = Flask(__name__)
app.secret_key = ' '.join(map(bin, bytearray(os.getenv("FLASK_SECRET")
                                             .encode('utf-8'))))

from courses_app import routes
