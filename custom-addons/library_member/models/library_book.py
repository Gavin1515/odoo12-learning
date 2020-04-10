#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields

class Book(models.Model):
    # _name是模型标识符，如果修改会发生什么呢？其实你可以修改，这时它会创建所继承模型的拷贝，成为一个新模型。这叫作原型继承
    _inherit = 'library.book'

    # 继承模型添加字段
    is_available = fields.Boolean(string='Is Available?')
    # 继承isbn字段，添加help帮助提示信息，其它属性自动继承
    isbn = fields.Char(help='Use a valid ISBN-13 or ISBN-10.')
    # 继承publisher_id字段，添加数据库索引属性，为该字段添加索引使查询更快，其它属性自动继承
    publisher_id = fields.Many2one(index=True)