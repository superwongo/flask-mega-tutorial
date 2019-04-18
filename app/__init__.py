#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# 实例化flask_sqlalchemy
db = SQLAlchemy()
# 实例化flask_migrate
migrate = Migrate()


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

    # 注册hello视图URL
    from app.hello import HelloWorld
    application.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))

    # 注册Login登录视图URL
    from app.login import LoginView
    application.add_url_rule('/login', view_func=LoginView.as_view('login'))

    try:
        # 确保 app.instance_path 存在
        os.makedirs(application.instance_path)
    except OSError:
        pass

    return application
