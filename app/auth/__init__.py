#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/7 17:32
# @File       : __init__.py

from flask import Blueprint


def register_views(bp):
    """注册视图类"""
    # 在函数中引入可以避免循环依赖问题
    from app.auth.views import LoginView, LogoutView, RegisterView, ResetPasswordRequestView, ResetPasswordView
    # 登录视图
    bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
    # 退出视图
    bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    # 注册视图
    bp.add_url_rule('/register', view_func=RegisterView.as_view('register'))
    # 申请重置密码视图
    bp.add_url_rule('/reset_password_request', view_func=ResetPasswordRequestView.as_view('reset_password_request'))
    # 重置密码视图
    bp.add_url_rule('/reset_password', view_func=ResetPasswordView.as_view('reset_password'))


# 创建用户认证蓝图
bp = Blueprint('auth', __name__)
# 注册视图类
register_views(bp)
