#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/15 10:01
# @File       : config

import os


# ----------FLASK-WTF扩展库配置--------- #
# 激活跨站点请求伪造保护
CSRF_ENABLED = True
# CSRF被激活时，用于令牌加密，表单验证
SECRET_KEY = 'you-will-never-guess'

# 配置SQLITE数据库信息
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 数据库文件存放路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'instance', 'flask.sqlite')
# Flask-SQLAlchemy 是否需要追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = False

