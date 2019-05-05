#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/19 11:26
# @File       : index

from flask.views import View
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from app import db
from app.forms import PostForm
from app.models import Post


class IndexView(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self):
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('你的帖子已提交！')
            return redirect(url_for('index'))

        # 获取本人及关注者对应的帖子信息
        page = request.args.get('page', 1, type=int)
        # 分页处理
        posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        # 下一页
        next_url = url_for('index', page=posts.next_num) if posts.has_next else None
        # 上一页
        prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
        return render_template('index/index.html', title='首页', form=form, posts=posts.items,
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
        next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
        # 上一页
        prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
        return render_template('index/index.html', title='发现', posts=posts.items,
                               next_url=next_url, prev_url=prev_url, page=page)
