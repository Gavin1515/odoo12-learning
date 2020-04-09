#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import fields, models, api
from odoo.exceptions import Warning

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

    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        isbn = self.isbn.replace('-', '')
        digits = [int(x) for x in isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi
    def action_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
            return True
