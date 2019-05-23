#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : Administrator
# @CreateTime : 2019/5/21 17:20
# @File       : __init__.py.py

from flask_restful import Api


def register_api(api):
    from app.api import users
    api.add_resource(users.GetUsers, '/api/get_users', endpoint='api.get_users')
    api.add_resource(users.GetUser, '/api/get_user/<int:id>', endpoint='api.get_user')


api = Api()
register_api(api)
