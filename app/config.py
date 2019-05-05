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


# ----------FLASK-SQLALCHEMY数据库配置---------#
# 配置SQLITE数据库信息
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 数据库文件存放路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'instance', 'flask.sqlite')
# Flask-SQLAlchemy 是否需要追踪对象的修改并且发送信号。
# 这需要额外的内存， 如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ----------EMAIL相关配置------------#
# 电子邮箱服务器
MAIL_SERVER = os.environ.get('MAIL_SERVER')
# 电子邮箱端口，标准端口为25
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
# 电子邮件服务器凭证默认不使用
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
# 电子邮箱服务器用户名
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# 电子邮箱服务器密码
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# 电子邮箱邮件接收地址
MAIL_ADMINS = ['1069291377@qq.com']

# -----------分页参数配置-------------#
# 每页展示数据条数
POSTS_PER_PAGE = 20
