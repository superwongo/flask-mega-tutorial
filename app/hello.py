#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/11 16:14
# @File       : hello

from flask.views import View


class HelloWorld(View):
    methods = ['GET']

    def dispatch_request(self):
        return 'Hello World!'
