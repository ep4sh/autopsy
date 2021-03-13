from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from courses_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cnest.db'
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_image = db.Column(db.String(20), default='default.jpg')
    docs = db.relationship('Doc', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_image}')"


class Doc(db.Model):
    doc_id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_content = db.Column(db.LargeBinary, nullable=False)
    doc_crc = db.Column(db.String(20), default='default.jpg')
    doc_created = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    doc_updated = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                        nullable=False)

    def __repr__(self):
        return f"Doc('{self.doc_name}', '{self.doc_crc}', \
                     '{self.doc_created}', '{self.doc_updated}')"
