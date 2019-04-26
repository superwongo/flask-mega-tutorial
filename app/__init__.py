#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os
import datetime
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_avatars import Avatars


# 实例化flask_sqlalchemy
db = SQLAlchemy()
# 实例化flask_migrate
migrate = Migrate()
# 实例化flask_login
lm = LoginManager()
# 实例化flask_avatars
avatars = Avatars()


def create_app():
    """应用工厂函数"""
    application = Flask(__name__)
    # 加载config配置文件
    application.config.from_pyfile('config.py', silent=True)

    # 初始化数据库flask_sqlalchemy
    db.init_app(application)

    # 初始化数据库flask_migrate
    import app.models
    migrate.init_app(application, db)

    # 初始化登录扩展flask_login
    lm.init_app(application)
    lm.login_view = 'login'
    lm.login_message = '请登录后访问此页面'

    # 初始化flask_avatars
    avatars.init_app(application)

    # 注册hello视图URL
    from app.hello import HelloWorld
    application.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))

    # 注册Login登录视图URL
    from app.login import LoginView
    application.add_url_rule('/login', view_func=LoginView.as_view('login'))

    # 注册Index首页视图URL
    from app.index import IndexView
    application.add_url_rule('/', view_func=IndexView.as_view('index'))

    # 注册Logout登出视图URL
    from app.login import LogoutView
    application.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

    # 注册Register注册视图URL
    from app.login import RegisterView
    application.add_url_rule('/register', view_func=RegisterView.as_view('register'))

    # 用户蓝图注册
    from app import user
    application.register_blueprint(user.bp)

    try:
        # 确保 app.instance_path 存在
        os.makedirs(application.instance_path)
    except OSError:
        pass

    @application.context_processor
    def utility_processor():
        """模板环境处理器注册"""
        def get_avatars(email, *args, **kwargs):
            """根据用户邮箱获取用户头像"""
            import hashlib
            email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
            return avatars.gravatar(email_hash, *args, **kwargs)
        return dict(get_avatars=get_avatars)

    @application.before_request
    def before_request():
        """请求前周期函数"""
        # 用户已登录则登记用户请求时间
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            db.session.commit()

    return application
