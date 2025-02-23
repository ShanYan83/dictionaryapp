from dictionaryapp.app import db
from flask_admin.contrib.sqla import ModelView
from wtforms_sqlalchemy.fields import QuerySelectField
from werkzeug.security import generate_password_hash
from wtforms import PasswordField
from flask_admin import Admin, AdminIndexView, expose
from flask_login import current_user
from flask import url_for,redirect
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(20), nullable=False) #unique name
    #users = db.relationship("User",back_populates='roles')
    # def __repr__(self):
    #     #return f'{self.rolename}'
    #     return f"{self.rolename}"

    def __repr__(self):
        #print(f"Accessing Role {self.id}")  # Debugging recursion calls
        return f"{self.rolename}"


class RoleView(ModelView):
    #can_delete = False
    #pass
    form_columns = ["rolename", "slug"]
    column_list = ["rolename", "slug"]
    def is_accessible(self):
        return current_user.is_authenticated  # ✅ Only logged-in users can access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("core.unauthorized"))
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))
    role = db.relationship("Role", backref="users")

    def __repr__(self):
        return f'Username: {self.username}'
    # def get_id(self):
    #     return self.id
    # def as_dict(self):
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    @property
    def is_active(self):
        return True  # Set to False if you want to deactivate a user

    @property
    def is_authenticated(self):
        return True  # User is authenticated after login

    @property
    def is_anonymous(self):
        return False  # Regular users are not anonymous

    def get_id(self):
        return str(self.id)  # Flask-Login needs this to identify the user
class UserAdmin(ModelView):
    form_columns = ["username", "email", "password", "role"]
    #column_exclude_list = ['password']
    column_list = ["username", "email", "role"]

    form_extra_fields = {
        'password': PasswordField('New Password')
    }

    form_overrides = {
        'role': QuerySelectField
    }
    form_args = {
        'role': {
            'query_factory': lambda: Role.query.all(),
            'get_label': lambda role: role.rolename
            #'get_label': lambda role: f"{role.slug}"
        }
    }
    # column_formatters = {
    #     "role": lambda v, c, m, p: m.role.rolename if m.role else "No Role"
    # }
    def on_model_change(self, form, model, is_created):
        if form.password.data:  # Only update if a new password is provided
            model.password = generate_password_hash(form.password.data)

    def is_accessible(self):
        return current_user.is_authenticated  # ✅ Only logged-in users can access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("core.unauthorized"))
# Custom Admin Dashboard (Prevents Anonymous Access)
class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("core.unauthorized"))  # ✅ Redirect anonymous users
        return self.render("admin/index.html", user=current_user)
