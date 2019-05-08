#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/8 14:57
# @File       : search.py

from flask import current_app


def add_to_index(index, model):
    """新增、修改索引"""
    # 未初始化elasticsearch实例，不进行处理
    if not current_app.elasticsearch:
        return

    # 获取需要检索的字段
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    # 将字段信息直接存入elasticsearch
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """删除索引"""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id, doc_type=index)


def query_index(index, query, page, per_page):
    """搜索"""
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page-1)*per_page,
              'size': per_page
              }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
