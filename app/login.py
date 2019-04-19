#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 9:37
# @File       : login

from flask.views import View
from flask import redirect, render_template, g, url_for, session, flash, request
from flask_login import login_user, logout_user

from app.forms import LoginForm
from app import lm, db
from app.models import User


@lm.user_loader
def load_user(id):
    """加载用户信息回调"""
    return User.query.get(int(id))


class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        # 若全局变量中已存在解析出的用户信息，且用户已验证通过，则直接跳转至首页
        if g.user and g.user.is_authenticated:
            return redirect(url_for('index'))

        # 加载登录Form表单
        form = LoginForm()
        # 登录Form表单提交验证通过，跳转至首页
        if form.validate_on_submit():
            flash('登录请求，用户{0}，记住我{1}'.format(form.username.data, form.remember_me.data))
            return redirect(url_for('index'))

        return render_template('login/login.html', title='登录', form=form)


# @oid.after_login
# def after_login(resp):
#     # 需要提供邮箱才能登录
#     if not resp.email:
#         flash('登录失败，请重试')
#         return redirect(url_for('login'))
#
#     # 通过邮件查询本地用户是否存在
#     user = User.query.filter_by(email=resp.email).first()
#     # 不存在用户，则登记用户信息
#     if not user:
#         nickname = resp.nickname
#         if not nickname:
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#
#     # 确认remember_me值
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     # 用户登录注册处理
#     login_user(user, remember=remember_me)
#     # 登录成功，跳转至下一页面
#     return redirect(request.args.get('next') or url_for('index'))


class LogoutView(View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))
