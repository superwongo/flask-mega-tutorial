#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 11:29
# @File       : models

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, nickname=None, email=None):
        self.nickname = nickname
        self.email = email

    @property
    def is_authenticated(self):
        """是否已验证"""
        return True

    @property
    def is_active(self):
        """是否处于活跃状态"""
        return True

    @property
    def is_anonymous(self):
        """是否为匿名用户"""
        return False

    def get_id(self):
        """获取用户唯一标识"""
        try:
            # python 2
            return unicode(self.id)
        except NameError:
            # python 3
            return str(self.id)

    def __repr__(self):
        """打印类对象时的展示方式"""
        return '<User %r>' % self.nickname


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>'.format(self.body)
