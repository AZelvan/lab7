from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/laba6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'any secret string'

db = SQLAlchemy(app)