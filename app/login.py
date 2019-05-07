#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 9:37
# @File       : login

from app import lm
from app.models import User


@lm.user_loader
def load_user(id):
    """加载用户信息回调"""
    return User.query.get(int(id))


