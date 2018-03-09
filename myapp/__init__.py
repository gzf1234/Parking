# -*- coding: utf8 -*-
#user:gzf

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from myapp.models import db

login_manager = LoginManager()
#session_protection会话的安全等级None,basic,strong
login_manager.session_protection = 'strong'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from myapp.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app