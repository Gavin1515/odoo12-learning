# -*- coding:utf-8 -*-
from odoo import api, fields, models, _

class Member(models.Model):
    _inherit = 'library.member'
    user_id = fields.Many2one('res.users')