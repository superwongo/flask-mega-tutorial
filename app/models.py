#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 11:29
# @File       : models

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    posts = relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, nickname=None, email=None):
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        """打印类对象时的展示方式"""
        return '<User %r>' % self.nickname


class Post(BaseModel):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>'.format(self.body)
