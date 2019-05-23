#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : Administrator
# @CreateTime : 2019/5/22 9:09
# @File       : extensions.py

from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_jwt import JWT

db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()
avatars = Avatars()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
jwt = JWT()


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)
    avatars.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    init_api(app)
    init_jwt(app)

    @babel.localeselector
    def get_locale():
        """获取本地语言环境"""
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def init_api(app):
    from app.api import api
    api.init_app(app)


def init_jwt(app):
    @jwt.authentication_handler
    def authenticate(username, password):
        from app.models import User
        user = User.query.filter(User.username == username).scalar()
        if user and user.check_password(password):
            return user

    @jwt.identity_handler
    def identify(payload):
        from app.models import User
        user_id = payload['identity']
        return User.query.filter(User.id == user_id).scalar()

    jwt.init_app(app)
