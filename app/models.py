#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 11:29
# @File       : models

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # index用于添加索引
    # unique用于设置唯一索引
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 初始化db.relationship
    # 并非实际的数据库字段，只是创建一个虚拟的列，该列会与 Post.user_id (db.ForeignKey) 建立联系
    # 第一个参数表示关联的模型类名；backref用于指定表之间的双向关系；lazy用于定义加载关联对象的方式
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, raw_password):
        """密码加密"""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """校验密码是否正确"""
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        """打印类对象时的展示方式"""
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.timezone)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>'.format(self.body)
