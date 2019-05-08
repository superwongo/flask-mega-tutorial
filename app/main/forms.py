#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/8 10:10
# @File       : forms.py

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_babel import lazy_gettext as _l

from app.models import User


class UserInfoEditForm(FlaskForm):
    """用户信息编辑表单"""
    username = StringField(_l('用户名'), validators=[DataRequired()])
    about_me = TextAreaField(_l('个人简介'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, *args, **kwargs):
        super(UserInfoEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('请使用其他用户名'))


class PostForm(FlaskForm):
    """帖子提交表单"""
    post = TextAreaField(_l('内容'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('提交'))


class SearchForm(FlaskForm):
    """搜索表单"""
    q = StringField(_l('搜索'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        # 由于选择GET的方式提交表单，所以通过request.args中获取参数
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        # 将csrf_enabled设置为False，设置Flask-WTF忽略此表单的CSRF验证。
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
