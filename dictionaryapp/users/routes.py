from flask import request, render_template,redirect,url_for, Blueprint,flash
from dictionaryapp.app import db
from dictionaryapp.users.models import User
users = Blueprint('users',__name__, template_folder='templates')
@users.route('/')
def index():
    users= User.query.all()
    #words=''
    return render_template('users/index.html',users=users)