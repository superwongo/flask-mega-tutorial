#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os
from flask import Flask


def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    # 加载config配置文件
    app.config.from_pyfile('config.py', silent=True)

    # 注册hello视图URL
    from app.hello import HelloWorld
    app.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))

    # 注册Login登录视图URL
    from app.login import LoginView
    app.add_url_rule('/login', view_func=LoginView.as_view('login'))

    try:
        # 确保 app.instance_path 存在
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
