# -*- coding:utf-8 -*-
from odoo import http
from odoo.http import request

class Main(http.Controller):

    @http.route('/checkouts', auth='user', website=True)
    def checkouts(self, **kwargs):
        checkout_obj = request.env['library.checkout']
        checkout_obj.invalidate_cache()
        checkouts = checkout_obj.search([])
        return request.render('library_website.index', {'docs': checkouts})

    # 注意这里路由使用了带有model(“library.checkout”)转换器的占位符，会映射到方法的 doc 变量中。
    # 它从 URL 中捕获借阅标识符，可以是简单的 ID 数值或链接别名，然后转换成相应的浏览记录对象。
    @http.route('/checkout/<model("library.checkout"):doc>', auth='user', website=True)
    def route(self, doc, **kwargs):
        return request.render('library_website.checkout', {'doc': doc})