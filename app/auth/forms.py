#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/7 17:32
# @File       : forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_babel import lazy_gettext as _l

from app.models import User


class LoginForm(FlaskForm):
    """登录表单"""
    # DataRequired：数据不可为空的验证器
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'), default=False)
    submit = SubmitField(_l('登录'))


class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('确认密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('注册'))

    def validate_username(self, username):
        """自定义username验证器"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l('该用户名已被使用'))

    def validate_email(self, email):
        """自定义email验证器"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_l('该邮箱已被使用'))


class ResetPasswordRequestForm(FlaskForm):
    """重置密码请求表单"""
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('请求密码重置'))


class ResetPasswordForm(FlaskForm):
    """重置密码表单"""
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('确认密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('请求密码重置'))
