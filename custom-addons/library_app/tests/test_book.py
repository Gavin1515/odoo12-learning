#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo.tests.common import TransactionCase

class TestBook(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        # 切换到admin用户测试该用户能否创建书，间接的测试了初始化安全组时是否正确加入了该用户
        self.env = self.env(user=self.env.ref('base.user_admin'))
        self.book = self.env['library.book']
        self.book_ode = self.book.create({
            'name': 'Odoo Development Essentials',
            'isbn': '879-1-78439-279-6'
        })

        return result

    def test_create(self):
        #"Test Books are active by default"
        self.assertEqual(self.book_ode.active, True)
