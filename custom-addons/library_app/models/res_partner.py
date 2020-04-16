#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # 测试在One2many一方添加ondelete="cascade"属性，删除出版商时并不会删除级联删除图书，所以建议在Many一方添加ondelete属性
    published_book_ids = fields.One2many(comodel_name="library.book", inverse_name="publisher_id",
                                         string="Published Books")
    # 如果Many2many关联的两个模型分别都有对应的Many2many字段，且都没有使用relation属性，那么它们会共用一张中间表。
    # relation可以自定义中间表名称以避免默认中间表可能超过63个字符的限制
    '''注意：在创建抽象模型时，many-to-many中不要使用column1和column2属性。
             在 ORM 设计中对抽象模型有一个限制，如果指定关联表列名，就无法再被正常继承。'''
    book_ids = fields.Many2many(comodel_name="library.book", string="Authored Books")