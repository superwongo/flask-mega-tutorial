#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 9:37
# @File       : login

from flask.views import View
from flask import flash, redirect, render_template, current_app

from app.forms import LoginForm


class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = LoginForm()
        if form.validate_on_submit():
            flash("登录请求，登录OpenID：{0}，是否记住我：{1}".format(form.openid.data, form.remember_me.data))
            return redirect('/index')
        return render_template('login/login.html',
                               title='登录',
                               form=form,
                               providers=current_app.config['OPENID_PROVIDERS'])
