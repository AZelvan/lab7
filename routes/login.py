from flask import Blueprint, request, render_template, redirect
from config import app, limiter
import hashlib
from routes.sign_up import register_form, login_form, Users
from flask_login import login_user
import requests
from time import sleep



first_route = Blueprint('first_route', __name__)

@app.route("/lab7")
def lab7():
    a = list(map(lambda x: x.get_data(), Users.query.all()))
    lena = len(a)
    for i in range(lena):
        s = a[i]
        print({'email': s[0], 'pwd': s[1]})
        data = {
                'email': s[0],
                'pwd': s[1]
                }
        data_response = requests.post('http://127.0.0.1:5000/loginpost', json=data)
        print(data_response.status_code)
        if data_response.status_code == '429':
            sleep(1)

    res = data_response.ok
    return {'code': res}



@app.route("/loginpost", methods=(["POST"]))
@limiter.limit("1 per minute")
def register_1():
        email = request.json['email']
        pwd = request.json['pwd']
        print(pwd)
        valid_email = list(map(lambda x: x.get_pass(), Users.query.filter_by(email=email)))
        if valid_email:
            pwd = hashlib.sha1(pwd.encode()).hexdigest()
            print(valid_email)
            if pwd == valid_email[0]:
                remember = True if request.form.get('remember') else False
                user = Users.query.filter_by(email=email).first()
                login_user(user, remember=remember)
                return redirect("/")
            error_body = {'reason': 'Try a different password'}
            return error_body
        error_body = {'reason': 'This email not exist'}
        return error_body

@app.route("/login")
def login():
    form = login_form()
    return render_template("login.html",form=form)


@app.route("/login", methods=(["POST"]))
def register():
    form = login_form()
    if form.validate_on_submit():
        email = form.email.data
        pwd = form.pwd.data
        valid_email = list(map(lambda x: x.get_pass(), Users.query.filter_by(email=email)))
        if valid_email:
            pwd = hashlib.sha1(pwd.encode()).hexdigest()
            print(valid_email)
            if pwd == valid_email[0]:
                remember = True if request.form.get('remember') else False
                user = Users.query.filter_by(email=email).first()
                login_user(user, remember=remember)
                return redirect("/")
            error_body = {'reason': 'Try a different password'}
            return render_template("login.html",res=error_body, form=form)
        error_body = {'reason': 'This email not exist'}
        return render_template('signup.html', res=error_body, form=form)
    error_body = {'reason': 'Form is not validate'}
    return render_template("login.html",res=error_body, form=form)