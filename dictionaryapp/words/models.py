from dictionaryapp.app import db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect,url_for
from wtforms_sqlalchemy.fields import QuerySelectField
class Locale(db.Model):
    __tablename__ = "locale"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    current = db.Column(db.Boolean, nullable=False, default=False)
    searchable = db.Column(db.Boolean, nullable=False, default=True)
    def __repr__(self):
        return f'Dialect: {self.language}'
    def get_id(self):
        return self.id
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def get_language(self):
        return f'{self.language}'
class LocaleView(ModelView):
    form_excluded_columns  = ["words"]
    def is_accessible(self):
        return current_user.is_authenticated  # ✅ Only logged-in users can access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("core.unauthorized"))
class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    eng_word = db.Column(db.String(20), nullable=False)
    eng_pos = db.Column(db.String(30), nullable=False)
    eng_meaning = db.Column(db.String(60), nullable=False)
    local_word = db.Column(db.String(20), nullable=False)
    local_pos = db.Column(db.String(30), nullable=False)
    local_meaning = db.Column(db.String(60), nullable=False)
    locale_id = db.Column(db.Integer, db.ForeignKey("locale.id"))
    local = db.relationship("Locale", backref="words")
    def __repr__(self):
        return f'English Word: {self.eng_word}'
    def get_id(self):
        return self.id
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
class WordView(ModelView):
    form_columns = ["eng_word", "eng_pos", "eng_meaning", "local_word", "local_pos", "local_meaning", "local"]
    column_list = ["eng_word", "eng_pos", "eng_meaning", "local_word", "local_pos", "local_meaning", "local"]
    form_overrides = {
        'local': QuerySelectField
    }
    form_args = {
        'local': {
            'query_factory': lambda: Locale.query.filter(Locale.current),
            'get_label': lambda local: local.language
            # 'get_label': lambda role: f"{role.slug}"
        }
    }
    def is_accessible(self):
        return current_user.is_authenticated  # ✅ Only logged-in users can access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("core.unauthorized"))
