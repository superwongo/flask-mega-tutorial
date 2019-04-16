#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/4/16 13:09
# @File       : database

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate

from app.config import SQLALCHEMY_DATABASE_URI

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
# 创建数据库会话
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))
# 创建数据库模型对象
BaseModel = declarative_base()
# 为数据库模型对象添加Query对象，用于数据库的查询操作
BaseModel.query = db_session.query_property()


def init_db():
    """初始化数据库，用于创建数据库表"""
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
    # 否则你就必须在调用 init_db() 之前导入它们。
    import app.models
    BaseModel.metadata.create_all(bind=engine)
    return BaseModel


def shutdown_session(exception=None):
    """关闭数据session"""
    db_session.remove()


def init_app(application):
    """初始化app，同时注册数据库模型"""
    # Flask 会自动在请求结束时或者应用关闭时删除数据库会话
    application.teardown_appcontext(shutdown_session)

    # 注册数据库模型
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在数据库迁移上。
    import app.models
    Migrate(application, BaseModel)
