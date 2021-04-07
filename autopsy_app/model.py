from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from autopsy_app import app, login_manager

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    # do not rename id - flask_login may become broken
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_image = db.Column(db.String(20), default='zombie.png')
    mortem = db.relationship('Mortem', backref='author', lazy=True)
    support_case = db.relationship('Support',
                                   backref='support_case_author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_email}', '{self.user_name}', \
                '{self.user_image}')"

    def generate_token(self, exprire_seconds=300):
        s = Serializer(app.config['SECRET_KEY'], exprire_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @classmethod
    def verify_token(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


class Mortem(db.Model):
    __tablename__ = 'mortems'
    id = db.Column(db.Integer, primary_key=True)
    mortem_name = db.Column(db.String(100), nullable=False)
    mortem_impact = db.Column(db.String(20), nullable=False)
    mortem_url = db.Column(db.String(16), nullable=False)
    mortem_content = db.Column(db.Text(), nullable=False)
    mortem_resolution = db.Column(db.Text())
    mortem_tags = db.Column(db.Text())
    mortem_created = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow)
    mortem_updated = db.Column(db.DateTime, nullable=False,
                               default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):
        return f"Mortem('{self.mortem_name}', '{self.user_id}', \
                     '{self.mortem_created}', '{self.mortem_updated}')"


class Support(db.Model):
    __tablename__ = 'support'
    id = db.Column(db.Integer, primary_key=True)
    support_subject = db.Column(db.String(100), nullable=False)
    support_content = db.Column(db.Text(), nullable=False)
    support_created = db.Column(db.DateTime, nullable=False,
                                default=datetime.utcnow)
    support_attach = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    def __repr__(self):
        return f"Support('{self.support_subject}', '{self.user_id}', \
                     '{self.support_created}', '{self.support_attach}')"
