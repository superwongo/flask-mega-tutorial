#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os

from flask import Flask
from flask_babel import lazy_gettext as _l
from elasticsearch import Elasticsearch
from redis import Redis
import rq

from app.extensions import db, migrate, lm, avatars, mail, bootstrap, moment, babel, register_extensions
from app.cli import register_commands
from app.logger import register_email, register_logger


def create_app(test_config=None):
    """应用工厂函数"""
    app = Flask(__name__)
    # --------------应用参数加载--------------- #
    # 加载config配置
    # 使用 config.py 中的值来重载缺省配置
    app.config.from_pyfile('config.py', silent=True)

    # test_config：单独设置配置参数，替代实例配置。这样可以实现 测试和开发的配置分离，相互独立。
    if test_config:
        app.config.from_mapping(test_config)

    # ---------注册Flask扩展库--- ---- #
    register_extensions(app)
    lm.login_view = 'auth.login'
    lm.login_message = _l('请登录后访问此页面')
    # ---------注册蓝图--------------- #
    register_blueprints(app)
    # ---------注册命令组------------- #
    # 翻译命令组注册
    register_commands(app)
    # ---------注册扩展功能属性-------- #
    register_attr(app)
    # ---------注册日志及异常提醒----- #
    # 非DEBUG模式下，异常日志通过电子邮件发送
    if not app.debug and not app.testing:
        # 异常日志邮件提醒初始化
        register_email(app)
        # 日志记录器初始化
        register_logger(app)

    # ---------实例目录创建----------- #
    try:
        # 确保 app.instance_path 存在
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app


def register_blueprints(app):
    # 用户认证子应用蓝图注册
    app.register_blueprint(auth.bp, url_prefix='/auth')
    # 错误子应用蓝图注册
    app.register_blueprint(errors.bp)
    # 核心子应用蓝图注册
    app.register_blueprint(main.bp)


def register_attr(app):
    # 添加Elasticsearch属性
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    # 添加redis属性
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)


from app import auth, errors, main, models
