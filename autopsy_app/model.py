from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from autopsy_app import app, login_manager

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    # do not rename id - flask_login may become broken
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_email = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_image = db.Column(db.String(20), default='zombie.png')
    mortem = db.relationship('Mortem', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_email}', '{self.user_name}', \
                '{self.user_image}')"


class Mortem(db.Model):
    __tablename__ = 'mortems'
    id = db.Column(db.Integer, primary_key=True)
    mortem_name = db.Column(db.String(100), nullable=False)
    mortem_url = db.Column(db.String(16), nullable=False)
    mortem_content = db.Column(db.Text(), nullable=False)
    mortem_created = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow)
    mortem_updated = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):
        return f"Mortem('{self.mortem_name}', '{self.user_id}', \
                     '{self.mortem_created}', '{self.mortem_updated}')"
