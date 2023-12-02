from flask import Blueprint, request, render_template, redirect
from config import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from config import app, login_manager
from flask_login import UserMixin
import hashlib


second_route = Blueprint('second_route', __name__)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)

    def get_data(self):
        return self.email, self.pwd

    def get_id(self):
        return self.id

    def get_pass(self):
        return self.pwd




@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class login_form(FlaskForm):
    email = StringField(validators=[DataRequired()])
    pwd = PasswordField(validators=[DataRequired()])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField('Войти')


class register_form(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    pwd = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


@app.route("/signup")
def signup():
    form = register_form()
    return render_template("signup.html",form=form)

@app.route("/signup", methods=(["POST"]))
def signup_1():
    form = register_form()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        pwd = form.pwd.data
        valid_email = list(map(lambda x: x.get_id(), Users.query.filter_by(email=email)))
        if valid_email == []:
            pwd = hashlib.sha1(pwd.encode()).hexdigest()
            new_user = Users(username=username, email=email, pwd=pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        error_body = {'reason': 'This email already exist'}
        return render_template('signup.html', res=error_body, form=form)
    error_body = {'reason': 'Form is not validate'}
    return render_template('signup.html', res=error_body, form=form)