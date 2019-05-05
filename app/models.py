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


followers = db.Table(
    # 表名
    'followers',
    # 关注者（粉丝）
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    # 被关注者
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


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
    # 个人介绍
    about_me = db.Column(db.String(140))
    # 最后访问时间
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # 当前用户的关注关系
    followed = db.relationship(
        # 关系当中的右侧实体（将左侧实体看成是上级类）
        'User',
        # 指定用于该关系的关联表
        secondary=followers,
        # 指明了通过关系表关联到左侧实体（关注者=粉丝）的条件
        # 关系中的左侧的join条件是关系表中的`follower_id`字段与这个关注者的用户ID匹配
        primaryjoin=(followers.c.follower_id == id),
        # 指明了通过关系表关联到右侧实体（被关注者）的条件
        secondaryjoin=(followers.c.followed_id == id),
        # 定义了右侧实体访问该关系的方式
        # 在左侧，关系被命名为followed，所以在右侧我将使用followers来表示所有左侧用户的列表，即粉丝列表
        # 附加的lazy参数表示这个查询的执行模式，设置为动态模式的查询不会立即执行，直到被调用
        backref=db.backref('followers', lazy='dynamic'),
        # 和backref中的lazy类似，只不过当前的这个是应用于左侧实体，backref中的是应用于右侧实体
        lazy='dynamic'
    )

    def set_password(self, raw_password):
        """密码加密"""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """校验密码是否正确"""
        return check_password_hash(self.password_hash, raw_password)

    def is_following(self, user):
        """是否存在关注关系"""
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        """添加关注"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """取消关注"""
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        """已关注用户帖子查询"""
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):
        """打印类对象时的展示方式"""
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>'.format(self.body)
