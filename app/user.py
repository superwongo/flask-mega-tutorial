#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/25 11:04
# @File       : user

from flask.views import View
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.models import User
from app.forms import UserInfoEditForm
from app import db

# 创建用户蓝图
bp = Blueprint('user', __name__, url_prefix='/user')


class UserInfoView(View):
    """用户信息查询"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        posts = [
            {'author': user, 'body': '测试1'},
            {'author': user, 'body': '测试2'},
        ]
        return render_template('user/user_info.html', user=user, posts=posts)


class UserInfoEditView(View):
    """用户资料编辑"""
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self):
        form = UserInfoEditForm(current_user.username)
        # 验证通过更新当前登录用户信息
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            # db.session.commit()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            flash('您的修改已保存')
            return redirect(url_for('user.user_info_edit'))
        elif request.method == 'GET':
            # 查询是获取当前用户的信息
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('user/user_info_edit.html', title='个人信息编辑', form=form)


# 将用户资料视图注册到用户蓝图上
bp.add_url_rule('/info/<username>', view_func=UserInfoView.as_view('user_info'))
# 将用户资料修改视图注册到用户蓝图上
bp.add_url_rule('/edit', view_func=UserInfoEditView.as_view('user_info_edit'))
