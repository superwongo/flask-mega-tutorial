#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/8 10:01
# @File       : __init__.py.py

import datetime

from flask import Blueprint, g
from flask_login import current_user
from flask_babel import get_locale

from app import avatars, db
from app.main.forms import SearchForm


def register_views(bp):
    # 在函数中引入可以避免循环依赖问题
    from app.main.views import IndexView, ExploreView, UserInfoView, UserInfoEditView, FollowView, \
        UnfollowView, SearchView, UserPopupView
    # 首页视图
    bp.add_url_rule('/', view_func=IndexView.as_view('index'))
    # 发现视图
    bp.add_url_rule('/explore', view_func=ExploreView.as_view('explore'))
    # 用户资料视图
    bp.add_url_rule('/info/<username>', view_func=UserInfoView.as_view('user_info'))
    # 用户资料修改视图
    bp.add_url_rule('/edit', view_func=UserInfoEditView.as_view('user_info_edit'))
    # 关注视图
    bp.add_url_rule('/follow/<username>', view_func=FollowView.as_view('follow'))
    # 取消关注视图
    bp.add_url_rule('/unfollow/<username>', view_func=UnfollowView.as_view('unfollow'))
    # 全局搜索视图
    bp.add_url_rule('/search', view_func=SearchView.as_view('search'))
    # 用户资料弹出框
    bp.add_url_rule('/info/<username>/popup', view_func=UserPopupView.as_view('user_popup'))

    @bp.before_request
    def before_request():
        """请求前周期函数"""
        # 用户已登录则登记用户请求时间
        if current_user.is_authenticated:
            current_user.last_seen = datetime.datetime.utcnow()
            db.session.commit()
            g.search_form = SearchForm()

        # 设置本地语言环境参数
        locale = get_locale()
        language = locale.language + '-' + locale.territory if locale.territory else locale.language
        g.locale = language

    @bp.context_processor
    def utility_processor():
        """模板环境处理器注册"""
        def get_avatars(email, *args, **kwargs):
            """根据用户邮箱获取用户头像"""
            import hashlib
            email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
            return avatars.gravatar(email_hash, *args, **kwargs)
        return dict(get_avatars=get_avatars)


# 创建用户蓝图
bp = Blueprint('main', __name__)
# 注册视图类
register_views(bp)
