#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/19 11:26
# @File       : index

from flask.views import View
from flask import render_template
from flask_login import login_required


class IndexView(View):
    methods = ['GET']
    decorators = [login_required]

    def dispatch_request(self):
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

        return render_template('index/index.html', title='首页', posts=posts)
