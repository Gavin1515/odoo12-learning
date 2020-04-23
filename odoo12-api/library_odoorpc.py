#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoorpc import ODOO

class LibraryAPI():
    def __init__(self, srv, port, db, user, pwd):
        # port参数必须要使用关键字参数，否则匹配不上
        self.api = ODOO(srv, port=port)
        self.api.login(db, user, pwd)
        self.uid = self.api.env.uid
        self.model = 'library.book'
        self.Model = self.api.env[self.model]

    def execute(self, method, arg_list, kwarg_dict=None):
        return self.api.execute(self.model, method, *arg_list, **kwarg_dict)

    def create(self, title):
        vals = {'name': title}
        return self.Model.create(vals)

    def write(self, title, id):
        vals = {'name': title}
        self.Model.write(id, vals)

    def unlink(self, id):
        return self.Model.unlink(id)

    def search_read(self, text=None):
        domain = [('name','ilike', text)] if text else []
        fields = ['id','name']
        return self.Model.search_read(domain, fields)
# 命令行调用python3 library.py的测试结果和使用XMLRPC实现的效果一样。