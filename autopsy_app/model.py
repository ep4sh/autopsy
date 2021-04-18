"""
Create DB Models for Autopsy Web App

Classes:
    - User(db.Model, UserMixin)
    - Role(db.Model)
    - UserRoles(db.Model)
    - Mortem(db.Model)
    - Support(db.Model)
"""
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, event
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from autopsy_app import app, login_manager

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    """
    Flask login manager user loader
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Represents User model

    Attributes:
        id : db.Column(db.Integer)
            User id, PK
        user_name : db.Column(db.String)
            User name
        user_email : db.Column(db.String)
            User email, must be uniq
        user_password : db.Column(db.String)
            User's password
        user_image : db.Column(db.String)
            User avatar from collection
        mortem : db.relationship
            User postmoretems (relationship)
        support_case : db.relationship
            User support_case requests (relationship)
        roles : db.relationship
            User roles (relationship)

    Methods:
        def generate_token(self, exprire_seconds=300) -> Serializer obj
        @classmethod def verify_token(self, token) -> User obj

    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_image = db.Column(db.String(20), default='zombie.png')
    mortem = db.relationship('Mortem', backref='author', lazy=True)
    support_case = db.relationship('Support',
                                   backref='support_case_author',
                                   lazy=True)
    roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        """
        User object string representation
        """
        return f"User('{self.user_email}', '{self.user_name}', \
                '{self.user_image}', '{self.roles}')"

    def generate_token(self, exprire_seconds=300):
        """
        Returns Serializer object UTF-8 string (token for password reset)
        """
        s_obj = Serializer(app.config['SECRET_KEY'], exprire_seconds)
        return s_obj.dumps({'user_id': self.id}).decode('utf-8')

    @classmethod
    def verify_token(cls, token):
        """
        Returns User object if verification successfully passed
        """
        s_obj = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s_obj.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


class Role(db.Model):
    """
    Represents role model

    Attributes:
        id : db.Column(db.Integer)
            Role id, PK
        name : db.Column(db.String)
            Role name

    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10), unique=True)

    def __repr__(self):
        """
        Role object string representation
        """
        return f"Role('{self.name}')"


class UserRoles(db.Model):
    """
    Represents User roles model

    Attributes:
        id : db.Column(db.Integer)
            UserRoles id, PK
        user_id : db.Column(db.Integer)
            User id relationship
        role_id : db.Column(db.Integer)
            Role id relationship

    """
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id',
                                                    ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id',
                                                    ondelete='CASCADE'))

    def __repr__(self):
        """
        UserRoles object string representation
        """
        return f"UserRoles('{self.user_id}', '{self.role_id}')"


class Mortem(db.Model):
    """
    Represents Mortem model

    Attributes:
        id : db.Column(db.Integer)
            Postmortem id, PK
        mortem_name : db.Column(db.String)
            Postmortem name
        mortem_impact : db.Column(db.String)
            Postmortem impact
        mortem_url = db.Column(db.String)
            Postmortem URL
        mortem_content = db.Column(db.Text)
            Postmortem body
        mortem_resolution = db.Column(db.Text)
            Postmortem resolution
        mortem_tags = db.Column(db.Text)
            Postmortem auto tags
        mortem_created = db.Column(db.DateTime)
            Postmortem creation date
        mortem_updated = db.Column(db.DateTime)
            Postmortem update date
        user_id = db.Column(db.Integer)
           Postmortem author (relationship)
    """
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
        """
        Mortem object string representation
        """
        return f"Mortem('{self.mortem_name}', '{self.user_id}', \
                     '{self.mortem_created}', '{self.mortem_updated}')"


class Support(db.Model):
    """
    Represents Mortem model

    Attributes:
        id : db.Column(db.Integer)
            Support case id, PK
        support_subject : db.Column(db.String)
            Support case subject
        support_content = db.Column(db.Text)
            Support case body
        support_created = db.Column(db.DateTime)
            Support case creation date
        user_id = db.Column(db.Integer)
           Support case author (relationship)
    """
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
        """
        Support object string representation
        """
        return f"Support('{self.support_subject}', '{self.user_id}', \
                     '{self.support_created}', '{self.support_attach}')"

@event.listens_for(Role.__table__, 'after_create')
def create_role(*args, **kwargs):
    """
    Create Autopsy role on app init
    """
    db.session.add(Role(name='admin'))
    db.session.add(Role(name='user'))
    db.session.commit()
