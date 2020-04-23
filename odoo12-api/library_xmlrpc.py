#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from xmlrpc import client

class LibraryAPI():
    # 处我们存储了所有创建执行模型调用的对象的所有信息：API引用、uid、密码、数据库名和要使用的模型。
    def __init__(self, srv, port, db, user, pwd):
        common = client.ServerProxy('http://%s:%d/xmlrpc/2/common' % (srv, port))
        self.api = client.ServerProxy('http://%s:%d/xmlrpc/2/object' % (srv, port))
        self.uid = common.authenticate(db, user, pwd, {})
        self.db = db
        self.pwd = pwd
        self.model = 'library.book'

    # 对odoo API的execute_kw方法进行封装
    def execute(self, method, arg_list, kwarg_dict=None):
        return self.api.execute_kw(self.db, self.uid, self.pwd, self.model, method, arg_list, kwarg_dict or {})

    def create(self, title):
        vals = {'name': title}
        return self.execute('create', [vals])

    def write(self, title, id):
        vals = {'name': title}
        return self.execute('write', [[id], vals])

    def unlink(self, id):
        return self.execute('unlink', [[id]])

    def search_read(self, text=None):
        domain = [('name', 'ilike', text)] if text else []
        fields = ['id', 'name']
        return self.execute('search_read', [domain, fields])

if __name__ == '__main__':
    srv, port, db, user, pwd = '192.168.99.116', 8069, 'dev12', 'admin', 'admin'
    api = LibraryAPI(srv, port, db, user, pwd)
    from pprint import pprint
    pprint(api.search_read())
    print(api.create("test1"))