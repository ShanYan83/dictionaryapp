from flask import render_template, Blueprint,request,flash,redirect,url_for
from dictionaryapp.words.models import Word,Locale
from dictionaryapp.users.models import User
from sqlalchemy import or_,and_
from werkzeug.security import check_password_hash
from flask_login import login_user,logout_user, current_user, login_required, LoginManager
core = Blueprint('core',__name__, template_folder='templates')
#@core.route('/admin')
#login_required()

@core.route('/')
def index():
    locales = Locale.query.filter(Locale.searchable == True)
    #locales = Locale.query.filter(Locale.id==4)
    return render_template('core/index.html',locales=locales)
@core.route('/unauthorized')
def unauthorized():
    return render_template('core/unauthorized.html')
@core.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have Successfully Logged out!')
    return redirect(url_for("core.login"))
def unauthorized():
    return render_template('core/unauthorized.html')
@core.route('/about')
def about():
    return render_template('core/about.html',action='admin-login')
@core.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('core/index.html',action='admin-login')
    if request.method == 'POST':
        if 'user_name' in request.form.keys():
            user_name = request.form['user_name']
            password = request.form.get('password')
            user = User.query.filter(User.username == user_name).first()
            if user is None:
                flash("User name does not exist!")
                return redirect(url_for('core.login'))
            elif check_password_hash(user.password,password):
                login_user(user)
                return redirect('/admin')
            else:
                flash("Incorrect Credentials!")
                return redirect(url_for('core.login'))
        # if login_id == 'shan' and login_pwd== '123':
        #     return 'Login Success'
        # else:
        #     return 'Login Failure'

@core.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('core/index.html', action='search')
    if request.method == 'POST':
        local_id = request.form.get('local_id')
        local = Locale.query.get_or_404(local_id)
        language = local.get_language()
        search_text = request.form.get('search_text')
        word = Word.query.filter(and_(or_(
                Word.eng_word.ilike(f"%{search_text}%"),
                Word.eng_meaning.ilike(f"%{search_text}%"),
                Word.local_word.ilike(f"%{search_text}%"),
                Word.local_meaning.ilike(f"%{search_text}%")
            ),Word.locale_id==local_id)).all()
        #word = Word.query.all()
        if not word:
            flash("No Matching word found!")
        locales = Locale.query.filter(Locale.searchable == True)
        #word = Word.query.filter(search_txt in Word.eng_word or search_txt in Word.local_word)
        return render_template('core/index.html', action='search',result=word,locales=locales,local_id=local_id,language=language)
