#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/5 9:55
# @File       : test_db

from datetime import datetime, timedelta

from app import db
from app.models import User, Post


def test_password_hashing():
    """测试密码加密"""
    u = User(username='susan')
    u.set_password('cat')
    assert u.check_password('dog') is False
    assert u.check_password('cat') is True


def test_follow(app):
    """测试关注函数"""
    with app.app_context():
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.followed.all() == []
        assert u1.followers.all() == []

        # john关注了susan
        u1.follow(u2)
        db.session.commit()
        assert u1.is_following(u2) is True
        # john用户信息的被关注者是susan
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'susan'
        # susan用户信息的关注者是john
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'john'

        # 解除关注
        u1.unfollow(u2)
        db.session.commit()
        assert u1.is_following(u2) is False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0


def test_follow_posts(app):
    """测试关注帖子获取函数"""
    with app.app_context():
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # john关注了susan
        u1.follow(u2)
        # john关注了david
        u1.follow(u4)
        # susan关注了mary
        u2.follow(u3)
        # mary关注了david
        u3.follow(u4)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        # john获取的帖子包括susan的、david的、自己的
        assert f1 == [p2, p4, p1]
        # susan获取的帖子包括mary的、自己的
        assert f2 == [p2, p3]
        # mary获取的帖子包括david的、自己的
        assert f3 == [p3, p4]
        # david获取的帖子只有自己的
        assert f4 == [p4]
