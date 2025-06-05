from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SECRET_KEY='strong secret key',
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@localhost/python-labs',
    CSRF_ENABLED = False,
    WTF_CSRF_ENABLED = False
)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

import urls
