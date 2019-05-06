#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 15:53
# @File       : __init__.py

import os
import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_avatars import Avatars
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment


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


def create_app(test_config=None):
    """应用工厂函数"""
    application = Flask(__name__)
    # 加载config配置
    # 使用 config.py 中的值来重载缺省配置
    application.config.from_pyfile('config.py', silent=True)

    # test_config：单独设置配置参数，替代实例配置。这样可以实现 测试和开发的配置分离，相互独立。
    if test_config:
        application.config.from_mapping(test_config)

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

    # 初始化flask_mail
    mail.init_app(application)

    # 初始化flask_bootstrap
    bootstrap.init_app(application)

    # 初始化flask_moment
    moment.init_app(application)

    # 注册hello视图URL
    from app.hello import HelloWorld
    application.add_url_rule('/hello', view_func=HelloWorld.as_view('hello'))

    # 注册Login登录视图URL
    from app.login import LoginView, LogoutView, RegisterView, ResetPasswordRequestView, ResetPasswordView
    application.add_url_rule('/login', view_func=LoginView.as_view('login'))

    # 注册Index首页视图URL
    from app.index import IndexView, ExploreView
    application.add_url_rule('/', view_func=IndexView.as_view('index'))
    # 注册Explore发现视图URL
    application.add_url_rule('/explore', view_func=ExploreView.as_view('explore'))

    # 注册Logout登出视图URL
    application.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

    # 注册Register注册视图URL
    application.add_url_rule('/register', view_func=RegisterView.as_view('register'))

    # 注册申请重置密码视图URL
    application.add_url_rule('/reset_password_request',
                             view_func=ResetPasswordRequestView.as_view('reset_password_request'))

    # 注册重置密码视图URL
    application.add_url_rule('/reset_password/<token>', view_func=ResetPasswordView.as_view('reset_password'))

    # 用户蓝图注册
    from app import user
    application.register_blueprint(user.bp)

    try:
        # 确保 app.instance_path 存在
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # 非DEBUG模式下，异常日志通过电子邮件发送
    if not application.debug:
        from app.logger import init_email, init_logger
        # 异常日志邮件提醒初始化
        init_email(application)
        # 日志记录器初始化
        init_logger(application)

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

    @application.errorhandler(404)
    def not_found_error(error):
        return render_template('error/404.html'), 404

    @application.errorhandler(500)
    def internal_error(error):
        return render_template('error/500.html'), 500

    return application
