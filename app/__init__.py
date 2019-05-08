#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_avatars import Avatars
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l


# 实例化flask_sqlalchemy
db = SQLAlchemy()
# 实例化flask_migrate
migrate = Migrate()
# 实例化flask_login
lm = LoginManager()
# 实例化flask_avatars
avatars = Avatars()
# 实例化flask_mail
mail = Mail()
# 实例化flask_bootstrap
bootstrap = Bootstrap()
# 实例化flask_moment
moment = Moment()
# 实例化flask_babel
babel = Babel()


def create_app(test_config=None):
    """应用工厂函数"""
    app = Flask(__name__)
    # 加载config配置
    # 使用 config.py 中的值来重载缺省配置
    app.config.from_pyfile('config.py', silent=True)

    # test_config：单独设置配置参数，替代实例配置。这样可以实现 测试和开发的配置分离，相互独立。
    if test_config:
        app.config.from_mapping(test_config)

    # 初始化数据库flask_sqlalchemy
    db.init_app(app)

    # 初始化数据库flask_migrate
    migrate.init_app(app, db)

    # 初始化登录扩展flask_login
    lm.init_app(app)
    lm.login_view = 'auth.login'
    lm.login_message = _l('请登录后访问此页面')

    # 初始化flask_avatars
    avatars.init_app(app)

    # 初始化flask_mail
    mail.init_app(app)

    # 初始化flask_bootstrap
    bootstrap.init_app(app)

    # 初始化flask_moment
    moment.init_app(app)

    # 初始化flask_babel
    babel.init_app(app)

    from app import auth, errors, main
    # 用户认证子应用蓝图注册
    app.register_blueprint(auth.bp, url_prefix='/auth')
    # 错误子应用蓝图注册
    app.register_blueprint(errors.bp)
    # 核心子应用蓝图注册
    app.register_blueprint(main.bp)

    # 翻译命令组注册
    from app.cli import register
    register(app)

    try:
        # 确保 app.instance_path 存在
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 非DEBUG模式下，异常日志通过电子邮件发送
    if not app.debug and not app.testing:
        from app.logger import init_email, init_logger
        # 异常日志邮件提醒初始化
        init_email(app)
        # 日志记录器初始化
        init_logger(app)

    return app


@babel.localeselector
def get_locale():
    """获取本地语言环境"""
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
