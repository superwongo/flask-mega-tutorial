#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/8 10:10
# @File       : views.py

from datetime import datetime

from flask import request, current_app, url_for, render_template, flash, redirect, g, jsonify
from flask.views import View
from flask_login import login_required, current_user
from flask_babel import _

from app import db
from app.models import User, Post, Message, Notification
from app.main.forms import UserInfoEditForm, PostForm, MessageForm


class IndexView(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self):
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash(_('你的帖子已提交！'))
            return redirect(url_for('main.index'))

        # 获取本人及关注者对应的帖子信息
        page = request.args.get('page', 1, type=int)
        # 分页处理
        posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        # 下一页
        next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
        # 上一页
        prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
        return render_template('index.html', title=_('首页'), form=form, posts=posts.items,
                               next_url=next_url, prev_url=prev_url, page=page)


class ExploreView(View):
    """发现视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        # 分页处理
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        # 下一页
        next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
        # 上一页
        prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
        return render_template('index.html', title=_('发现'), posts=posts.items,
                               next_url=next_url, prev_url=prev_url, page=page)


class UserInfoView(View):
    """用户信息查询"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        page = request.args.get('page', 1, type=int)
        posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.user_info', username=user.username, page=posts.next_num) if posts.has_next else None
        prev_url = url_for('main.user_info', username=user.username, page=posts.prev_num) if posts.has_prev else None
        return render_template('user_info.html', user=user, posts=posts.items,
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
            return redirect(url_for('main.user_info_edit'))
        elif request.method == 'GET':
            # 查询是获取当前用户的信息
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('user_info_edit.html', title=_('个人信息编辑'), form=form)


class FollowView(View):
    """关注视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('用户%(username)s未找到', username=username))
            return redirect(url_for('main.index'))
        elif user == current_user:
            flash(_('不能关注自己！'))
            return redirect(url_for('main.user_info', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('您已关注%(username)s！', username=username))
        return redirect(url_for('main.user_info', username=username))


class UnfollowView(View):
    """取消关注视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            flash(_('用户%(username)s未找到', username=username))
            return redirect(url_for('main.index'))
        elif user == current_user:
            flash(_('不能取消关注自己！'))
            return redirect(url_for('main.user_info', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('您已取消关注%(username)s！', username=username))
        return redirect(url_for('main.user_info', username=username))


class SearchView(View):
    """搜索视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
        # 表单校验失败，跳转至发现页
        if not g.search_form.validate():
            return redirect(url_for('main.explore'))
        # 分页查询
        page = request.args.get('page', 1, type=int)
        posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
        next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) \
            if total > page*current_app.config['POSTS_PER_PAGE'] else None
        prev_url = url_for('main.search', q=g.search_form.q.data, page=page-1) \
            if page > 1 else None
        return render_template('search.html', title=_('搜索'), posts=posts,
                               page=page, next_url=next_url, prev_url=prev_url)


class UserPopupView(View):
    """用户资料弹出框"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self, username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('user_popup.html', user=user)


class SendMessageView(View):
    """发送私信视图"""
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, recipient):
        user = User.query.filter_by(username=recipient).first_or_404()
        form = MessageForm()
        if form.validate_on_submit():
            msg = Message(author=current_user, recipient=user, body=form.message.data)
            db.session.add(msg)
            user.add_notification('unread_message_count', user.new_messages())
            db.session.commit()
            flash(_('您的消息已被发送'))
            return redirect(url_for('main.user_info', username=recipient))
        return render_template('send_message.html', title=_('发送消息'), form=form, recipient=recipient)


class MessageView(View):
    """私信视图"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
        # 更新私信最后查看时间
        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        messages = current_user.messages_received.order_by(
            Message.timestamp.desc()).paginate(
                page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.messages', page=messages.next_num) if messages.has_next else None
        prev_url = url_for('main.messages', page=messages.prev_num) if messages.has_prev else None
        return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url, page=page)


class NotificationView(View):
    """通知"""
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
        # 实现通过查询条件，来限制只请求给定时间戳之后产生的通知
        since = request.args.get('since', 0.0, type=float)
        notifications = current_user.notifications.filter(
            Notification.timestamp > since).order_by(Notification.timestamp.asc())
        return jsonify([{'name': n.name, 'data': n.get_data(), 'timestamp': n.timestamp} for n in notifications])
