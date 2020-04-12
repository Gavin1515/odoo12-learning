#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields, api

class Book(models.Model):
    # _name是模型标识符，如果修改会发生什么呢？其实你可以修改，这时它会创建所继承模型的拷贝，成为一个新模型。这叫作原型继承
    _inherit = 'library.book'

    # 继承模型添加字段
    is_available = fields.Boolean(string='Is Available?')
    # 继承isbn字段，添加help帮助提示信息，其它属性自动继承
    isbn = fields.Char(help='Use a valid ISBN-13 or ISBN-10.')
    # 继承publisher_id字段，添加数据库索引属性，为该字段添加索引使查询更快，其它属性自动继承
    publisher_id = fields.Many2one(index=True)


    # 继承_check_isbn方法，增加10位isbn的校验逻辑
    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        isbn = self.isbn.replace('-', '')
        digits = [int(x) for x in isbn if x.isdigit()]
        if len(digits) == 10:
            ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            total = sum(a * b for a, b in zip(digits[:9], ponderators))
            check = total % 11
            return digits[-1] == check
        else:
            # 从odoo11开始，super()无需传入类名和self两个参数
            return super()._check_isbn()
