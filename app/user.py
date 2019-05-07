#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/25 11:04
# @File       : user

from flask.views import View
from flask import render_template, Blueprint, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from flask_babel import _

from app.models import User, Post
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
        page = request.args.get('page', 1, type=int)
        posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('user.user_info', username=user.username, page=posts.next_num) if posts.has_next else None
        prev_url = url_for('user.user_info', username=user.username, page=posts.prev_num) if posts.has_prev else None
        return render_template('user/user_info.html', user=user, posts=posts.items,
                               next_url=next_url, prev_url=prev_url, page=page)


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
            flash(_('您的修改已保存'))
            return redirect(url_for('user.user_info_edit'))
        elif request.method == 'GET':
            # 查询是获取当前用户的信息
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('user/user_info_edit.html', title=_('个人信息编辑'), form=form)


class FollowView(View):
    """关注视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('用户%(username)s未找到', username=username))
            return redirect(url_for('index'))
        elif user == current_user:
            flash(_('不能关注自己！'))
            return redirect(url_for('user.user_info', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('您已关注%(username)s！', username=username))
        return redirect(url_for('user.user_info', username=username))


class UnfollowView(View):
    """取消关注视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('用户%(username)s未找到', username=username))
            return redirect(url_for('index'))
        elif user == current_user:
            flash(_('不能取消关注自己！'))
            return redirect(url_for('user.user_info', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('您已取消关注%(username)s！', username=username))
        return redirect(url_for('user.user_info', username=username))


# 将用户资料视图注册到用户蓝图上
bp.add_url_rule('/info/<username>', view_func=UserInfoView.as_view('user_info'))
# 将用户资料修改视图注册到用户蓝图上
bp.add_url_rule('/edit', view_func=UserInfoEditView.as_view('user_info_edit'))

# 将关注视图注册到用户蓝图上
bp.add_url_rule('/follow/<username>', view_func=FollowView.as_view('follow'))
# 将取消关注视图注册到用户蓝图上
bp.add_url_rule('/unfollow/<username>', view_func=UnfollowView.as_view('unfollow'))
