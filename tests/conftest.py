#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/30 10:59
# @File       : conftest

import os
import tempfile

import pytest

from app import create_app, db

# 加载初始化SQL语句文件
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.readlines()


@pytest.fixture
def app():
    """初始化应用实例、数据库"""
    # tempfile.mkstemp() 创建并打开一个临时文件，返回该文件对象和路径。
    # DATABASE 路径被重载，这样它会指向临时路径，而不是实例文件夹。
    db_fd, db_path = tempfile.mkstemp()

    # TESTING：设置 Flask 应用处在测试模式下。
    app = create_app({
        'TESTING': True,
        # 数据库文件存放路径
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path
    })

    # 加载应用环境
    with app.app_context():
        # 初始化数据库模型
        db.create_all()
        # 循环执行初始化SQL
        for sql in _data_sql:
            if sql:
                db.engine.execute(sql.decode('utf8'))

    yield app

    # 再次创建APP时，会删除原临时数据库文件，进行数据库重新初始化
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """用于调用由 app 固件创建的应用 对象"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建一个运行器，用于调用应用注册的 Click 命令"""
    return app.test_cli_runner()
