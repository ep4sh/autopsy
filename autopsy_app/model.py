from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from autopsy_app import app, login_manager

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # do not rename id - flask_login may become broken
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_email = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_image = db.Column(db.String(20), default='default.jpg')
    docs = db.relationship('Doc', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_email}', '{self.user_name}', '{self.user_image}')"


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_content = db.Column(db.LargeBinary, nullable=False)
    doc_crc = db.Column(db.String(20), default='default.jpg')
    doc_created = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    doc_updated = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __repr__(self):
        return f"Doc('{self.doc_name}', '{self.doc_crc}', \
                     '{self.doc_created}', '{self.doc_updated}')"
