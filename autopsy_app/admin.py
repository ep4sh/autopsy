"""
Create Admin page for Autopsy Web App

Classes:
   - AutopsyModelView(sqla.ModelView):
   - AutopsyAdminIndexView(admin.AdminIndexView):
"""
import flask_admin as admin
from flask import abort
from flask_admin import helpers, expose, Admin
from flask_admin.contrib import sqla
from flask_login import current_user
from autopsy_app import app
from autopsy_app.model import db, User, Mortem, Support, Role


# Create customized model view class
class AutopsyModelView(sqla.ModelView):
    """
    Represents AutopsyModelView - admin model

    Methods:
        is_accessible -> bool
        inaccessible_callback -> redirect
    """

    def is_accessible(self):
        return bool(current_user.id == 1 and current_user.is_authenticated)

    def inaccessible_callback(self, name, **kwargs):
        # abort to access login page if user doesn't have access
        return abort(403)


# Create customized index view class that handles login & registration
class AutopsyAdminIndexView(admin.AdminIndexView):
    """
    Represents AutopsyAdminIndexView - admin panel index view

    Methods:
        def index -> redirect / render
    """

    @expose('/')
    def index(self):
        if current_user.is_anonymous or current_user.id != 1:
            return abort(403)
        return super(AutopsyAdminIndexView, self).index()


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
adm = Admin(app, index_view=AutopsyAdminIndexView())
# magic of flask_admin
adm.add_view(AutopsyModelView(User, db.session))
adm.add_view(AutopsyModelView(Mortem, db.session))
adm.add_view(AutopsyModelView(Support, db.session))
adm.add_view(AutopsyModelView(Role, db.session))
