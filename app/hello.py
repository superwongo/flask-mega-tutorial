#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 16:14
# @File       : hello

from flask.views import View
from flask import render_template


class HelloWorld(View):
    methods = ['GET']

    def dispatch_request(self):
        user = {'nickname': 'Super.Wong'}
        posts = [
            {
                'author': {'nickname': '李白'},
                'body': '举头望明月，低头思故乡'
            },
            {
                'author': {'nickname': '李清照'},
                'body': '知否，知否，应是绿肥红瘦'
            }
        ]
        return render_template('hello/hello.html', title='测试', user=user, posts=posts)
