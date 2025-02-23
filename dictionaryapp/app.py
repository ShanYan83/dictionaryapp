from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
admin = Admin()

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static', static_url_path='/')
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tenyidie.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dictionary_db'
    app.secret_key = "SecureKey"
    app.config['LOCAL'] = 'Tenyidie';
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from dictionaryapp.users.models import SecureAdminIndexView
    admin.init_app(app,index_view=SecureAdminIndexView())
    #import and register all blueprints
    from dictionaryapp.core.routes import core
    from dictionaryapp.words.routes import words
    from dictionaryapp.users.routes import users
    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(words,url_prefix='/words')
    app.register_blueprint(users, url_prefix='/users')
    from dictionaryapp.words.models import Word
    from dictionaryapp.words.models import Locale
    from dictionaryapp.users.models import RoleView
    from dictionaryapp.users.models import Role
    from dictionaryapp.users.models import User
    #from dictionaryapp.users.models import UserView
    from dictionaryapp.users.models import UserAdmin
    from dictionaryapp.words.models import WordView
    from dictionaryapp.words.models import LocaleView
    from flask_admin.contrib.sqla import ModelView
    #admin.add_view(ModelView(Word, db.session))
    admin.add_view(RoleView(Role, db.session))
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(LocaleView(Locale, db.session))
    admin.add_view(WordView(Word, db.session))
    #admin.add_view(UserView(User, db.session,name="Users",menu_icon_type="fa",menu_icon_value="fa user"))

    migrate = Migrate(app, db)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    from flask import redirect,url_for
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        #return redirect(url_for("core.unauthorized", next=request.url))
        return redirect(url_for("core.unauthorized"))
    #from routes
    return app