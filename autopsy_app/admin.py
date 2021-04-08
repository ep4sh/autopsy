import flask_admin as admin
from flask import redirect, url_for, abort
from flask_admin import helpers, expose, Admin
from flask_admin.contrib import sqla
from flask_login import current_user
from autopsy_app import app
from autopsy_app.model import db, User, Mortem, Support, Role


# Create customized model view class
class AutopsyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.id == 1 and current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return abort(403)


# Create customized index view class that handles login & registration
class AutopsyAdminIndexView(admin.AdminIndexView):

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
