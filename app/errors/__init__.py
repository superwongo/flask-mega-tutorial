#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/8 9:49
# @File       : __init__.py

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
