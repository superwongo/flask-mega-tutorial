#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project    : flask-mega-tutorial
# @Author     : wangc
# @CreateTime : 2019/5/6 9:55
# @File       : email

from threading import Thread

from flask_mail import Message
from flask import current_app

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    发送电子邮件
    :param subject: 标题
    :param sender: 发送者
    :param recipients: 接收者列表
    :param text_body: 纯文本内容
    :param html_body: HTML格式内容
    :return:
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
