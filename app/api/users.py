#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : Administrator
# @CreateTime : 2019/5/21 17:24
# @File       : users.py

from flask_restful import Resource, fields, marshal_with
from flask_jwt import jwt_required

from app.models import User


class LastSeenItem(fields.Raw):
    def format(self, value):
        return value.isoformat() + 'Z'


class RelationshipCountItem(fields.Raw):
    def format(self, value):
        return value.count()


users_fields = {
    'id': fields.Integer,
    'name': fields.String(attribute='username', default='Anonymous User'),
    'last_seen': LastSeenItem(attribute='last_seen'),
    'about_me': fields.String,
    'post_count': RelationshipCountItem(attribute='posts'),
    'follower_count': RelationshipCountItem(attribute='follower'),
    'followed_count': RelationshipCountItem(attribute='followed'),
    '_links': {
        'self': fields.Url('api.get_user', absolute=True),
        # 'follower': fields.Url('api.get_followers', absolute=True),
        # 'followed': fields.Url('api.get_followed', absolute=True)
    }
}


class GetUsers(Resource):
    @marshal_with(users_fields, envelope='resource')
    @jwt_required()
    def get(self):
        return User.query.all()


class GetUser(Resource):
    @marshal_with(users_fields, envelope='resource')
    @jwt_required()
    def get(self, id):
        return User.query.filter_by(id=id).first()
