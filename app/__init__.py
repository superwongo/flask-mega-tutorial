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
    # instance_relative_config：设置配置文件以instance文件夹为相对文件夹
    # 即config.py配置文件放置在instance文件夹下。
    app = Flask(__name__, instance_relative_config=True)

    # 注册hello视图URL
    from app.hello import HelloWorld
    app.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))

    try:
        # 确保 app.instance_path 存在
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
