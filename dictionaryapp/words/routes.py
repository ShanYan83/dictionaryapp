from flask import request, render_template,redirect,url_for, Blueprint,flash
from dictionaryapp.app import db
from dictionaryapp.words.models import Word
from flask_login import login_required
words = Blueprint('words',__name__, template_folder='templates')
@words.route('/')
@login_required
def index():
    words= Word.query.all()
    #words=''
    return render_template('words/index.html',words=words)
@words.route('/create',methods=['GET','POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('words/create.html')
    if request.method == 'POST':
        eng_word = request.form.get('eng_word')
        eng_pos = request.form.get('eng_pos')
        eng_meaning = request.form.get('eng_meaning')
        local_word = request.form.get('local_word')
        local_pos = request.form.get('local_pos')
        local_meaning = request.form.get('local_meaning')
        msg="Word Added Successfully!"
        if request.form.get('id'):
            id=request.form.get('id')
            word = Word.query.get_or_404(id)
            word.eng_word = eng_word
            word.eng_pos = eng_pos
            word.eng_meaning = eng_meaning
            word.local_word = local_word
            word.local_pos = local_pos
            word.local_meaning = local_meaning
            msg = "Word Updated Successfully!"
        else:
            word = Word(eng_word=eng_word, eng_pos=eng_pos,eng_meaning=eng_meaning,local_word=local_word,local_pos=local_pos,local_meaning=local_meaning)
            db.session.add(word)
        db.session.commit()
        flash(msg)
        return redirect(url_for('words.index'))

@words.route('/delete/<id>',methods=['DELETE'])
@login_required
def delete(id):
    Word.query.filter(Word.id==id).delete()
    db.session.commit()
    words = Word.query.all()
    # words=''
    return render_template('words/index.html', words=words)
@words.route('/edit/<id>')
@login_required
def edit(id):
    word = Word.query.get_or_404(id).as_dict()
    #word_dict = [w.as_dict() for w in word]
    #word = Word.getItem(Word.query.get_or_404(id))
    #db.session.commit()
    return render_template('words/create.html', word=word)

