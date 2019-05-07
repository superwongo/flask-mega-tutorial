#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/7 15:29
# @File       : cli

import os
import click


def register(app):
    """翻译命令行注册"""
    @app.cli.group()
    def translate():
        """翻译命令组"""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """
        初始化新语言
        :param lang: 语言代码
        :return:
        """
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract命令失败')
        if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init命令失败')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """更新子命令"""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract命令失败')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update命令失败')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """编译子命令"""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile命令失败')
