#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import fields, models

class Book(models.Model):
    _name = 'library.book' # 仅有模型名使用点号(.) 来分割关键字，其它如模块、XML 标识符、数据表名等都使用下划线(_)
    _description = 'Book'

    name = fields.Char(string='Title', required=True)
    isbn = fields.Char(string='ISBN')
    active = fields.Boolean(string='Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary(string='Cover')
    publisher_id = fields.Many2one(comodel_name='res.partner', string='Publisher')
    author_ids = fields.Many2many(comodel_name='res.partner', string="Authors")
