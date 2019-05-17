#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 11:29
# @File       : models

import json
from datetime import datetime
import jwt
from time import time

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app

from app import db, lm
from app.search import query_index, add_to_index, remove_from_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        """搜索"""
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        # 根据查询出的对象ID匹配对象信息
        # CASE语句，用于确保查询出的数据库中的结果与给定ID的顺序相同
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)
        ), total

    @classmethod
    def before_commit(cls, session):
        """会话提交前，记录对象变更"""
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        """会话提交后，根据记录的变更同步elasticsearch"""
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """用于初始化数据库已有数据"""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


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
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
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
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

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

    def get_jwt_token(self, expires_in=600):
        """获取JWT令牌"""
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf8')

    @staticmethod
    def verify_jwt_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.get(user_id)

    def new_messages(self):
        """查询用户未读信息条数"""
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        """新增通知"""
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        db.session.commit()
        return n

    def __repr__(self):
        """打印类对象时的展示方式"""
        return '<User %r>' % self.username


@lm.user_loader
def load_user(id):
    """加载用户信息回调"""
    return User.query.get(int(id))


class Post(SearchableMixin, db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % self.body


# 增加监听Post模型的提交事件
db.event.listen(db.session, 'before_commit', Post.before_commit)
db.event.listen(db.session, 'after_commit', Post.after_commit)


class Message(db.Model):
    """私信"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    """通知"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
