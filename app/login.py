#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 9:37
# @File       : login

from flask.views import View
from flask import redirect, render_template, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user

from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
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
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        # 加载登录Form表单
        form = LoginForm()
        # 登录Form表单提交验证通过，跳转至首页
        if form.validate_on_submit():
            # 根据用户名查询本地用户信息
            user = User.query.filter_by(username=form.username.data).first()
            # 用户不存在或密码校验失败，增加闪现消息，并重定向到登录页
            if not user or not user.check_password(form.password.data):
                flash('用户名或密码有误')
                return redirect(url_for('login'))

            # 用户校验通过，进行用户登录，并重定向到首页
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', '')
            if not next_page or not url_parse(next_page).decode_netloc():
                next_page = url_for('index')
            return redirect(next_page)

        # GET请求，直接展示登录页面
        return render_template('login/login.html', title='登录', form=form)


class LogoutView(View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))


class RegisterView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return url_for('index')

        form = RegistrationForm()
        # 校验成功，创建用户信息，跳转至登录页面
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('祝贺，你现在已成为一个注册用户！')
            return redirect(url_for('login'))

        return render_template('login/register.html', title='注册', form=form)


class ResetPasswordRequestView(View):
    """重置密码申请视图"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                flash('该电子邮箱未注册')
                return redirect(url_for('reset_password_request'))

            from app.email import send_password_reset_email
            send_password_reset_email(user)
            flash('查看您的电子邮箱消息，以重置您的密码')
            return redirect(url_for('login'))
        return render_template('login/reset_password_request.html', title='重置密码', form=form)


class ResetPasswordView(View):
    """重置密码视图"""
    methods = ['GET', 'POST']

    def dispatch_request(self, token):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        user = User.verify_jwt_token(token)
        if not user:
            return redirect(url_for('index'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            db.session.commit()
            flash('您的密码已被重置')
            return redirect(url_for('login'))
        return render_template('login/reset_password.html', form=form)
