#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import http
from odoo.addons.library_app.controllers.main import Books

class BookExtended(Books):

    '''
        继承controller,在url中添加available参数：library/books?available=1。
        如果不带参数，将会保留父类中定义的路由。
        但也可以为@http.route()装饰器添加参数，来重新定义或替换类路由。
        例如：可以@http.route('/getbooks')来替换原来的/librayr/books路由，但是原/librayr/books就不可用了
    '''
    @http.route()
    def list(self, **kwargs):
        response = super().list(**kwargs)
        # 请求参数会封装到kwargs里面
        if kwargs.get('available'):
            books = http.request.env['library.book'].search([('is_available','=',True)])
            response.qcontext['books'] = books
        return response