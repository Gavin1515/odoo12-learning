#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields, api, exceptions

class Checkout(models.Model):
    _name = 'library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread','mail.activity.mixin']

    member_id = fields.Many2one(comodel_name='library.member', required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Librarion', default=lambda s: s.env.uid)
    request_date = fields.Date(default=lambda s: fields.Date.today())
    line_ids = fields.One2many(comodel_name='library.checkout.line',inverse_name='checkout_id', string='Borrowed Books')

    @api.model
    def _default_stage(self):
        return self.env['library.checkout.stage'].search([], limit=1)
    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)
    '''
        group_expand参数重载字段的分组方式，默认的分组操作行为是仅能看到使用过的阶段，而不带有借阅文档的阶段不会显示。
        在我们的例子中，我们想要不同的效果：我们要看到所有的阶段，
        哪怕它没有文档。_group_expand_stage_id() 帮助函数返回分组操作需使用组记录列表。
        本例中返回所有已有阶段，不论其中是否包含图书借阅记录。

        Odoo 10中的修改: group_expand字段在Odoo 10中引入，但在官方文档中没有介绍.
    '''
    stage_id = fields.Many2one(comodel_name='library.checkout.stage', default=_default_stage,
                               group_expand = '_group_expand_stage_id')
    state = fields.Selection(related='stage_id.state')
    checkout_date = fields.Date(readonly=True)
    closed_date = fields.Date(readonly=True)

    @api.onchange('member_id')
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = today
            return {
                'warning':{
                    'title': 'Changed Request Date',
                    'message': 'Request date change to today.'
                }
            }
        '''
            change方法还可以返回字段上的域限制字段取值范围：
            {‘user_id’: [(’email’, ‘!=’, False)]}
        '''
    @api.model
    def create(self, vals):
        # Code before create: should use the `vals` dict
        if 'stage_id' in vals:
            Stage = self.env['library.checkout.stage']
            new_state = Stage.browse(vals['stage_id']).state
            if new_state == 'open':
                vals['checkout_date'] = fields.Date.today()
        new_record = super().create(vals)
        # Code after create: can use the `new_record` created
        if new_record.state == 'done':
            raise exceptions.UserError('Not allowed to create a checkout in the done state.')
        return new_record


class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'

    checkout_id = fields.Many2one(comodel_name='library.checkout')
    book_id = fields.Many2one(comodel_name='library.book')