#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/9 17:57
# @File       : microblog.py


from app import create_app, db
from app.models import User, Post, Message, Notification, Task


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification, 'Task': Task}
