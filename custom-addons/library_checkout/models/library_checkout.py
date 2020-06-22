#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields, api, exceptions

class Checkout(models.Model):
    _name = 'library.checkout'
    _description = 'Checkout Request'
    _inherit = ['mail.thread','mail.activity.mixin']

    # track_visibility='onchange'表示带有该属性值的字段在被修改时记录到message中，但是track_visibility='onchange'不起作用。
    member_id = fields.Many2one(comodel_name='library.member', required=True, track_visibility='onchange')
    user_id = fields.Many2one(comodel_name='res.users', string='Librarion', default=lambda s: s.env.uid,
                              track_visibility='onchange')
    request_date = fields.Date(default=lambda s: fields.Date.today(), track_visibility='always')
    line_ids = fields.One2many(comodel_name='library.checkout.line',inverse_name='checkout_id', string='Borrowed Books')
    num_other_checkouts = fields.Integer(compute='_compute_num_other_checkouts')

    def _compute_num_other_checkouts(self):
        for checkout in self:
            domain = [('member_id','=',checkout.member_id.id),('state','in',['open']),('id','!=',checkout.id)]
            checkout.num_other_checkouts = self.search_count(domain)

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
    member_image = fields.Binary(related='member_id.partner_id.image')
    num_books = fields.Integer(compute='_compute_num_books', store=True)
    # 让用户组织他们的工作项，标记什么应优先处理
    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Normal'),
         ('2', 'High')],
        'Priority',
        default='1')
    # 标记是否应移向下一阶段或因某种原因原地不动
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('blocked', 'Blocked'),
         ('done', 'Ready for next stage')],
        'Kanban State',
        default='normal')
    # 用于存储看板卡片显示的颜色，并可通过看板视图中的颜色拾取器菜单设置
    color = fields.Integer(string='Color Index')

    @api.depends('line_ids')
    def _compute_num_books(self):
        for checkout in self:
            checkout.num_books = len(checkout.line_ids)

    @api.onchange('member_id')
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date and self.request_date != today:
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
    # 自odoo12开始，create()现在也可批量创建数据，这通过把单个字典对象修改为字典对象列表来传参进行实现。
    # 这由带有@api.model_create_multi装饰器的create() 方法来进行支持。
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

    @api.multi
    def write(self, vals):
        for checkout in self:
            # Code before write: can use `self`, with the old values
            if 'stage_id' in vals:
                new_state = self.env['library.checkout.stage'].browse(vals['stage_id']).state
                if new_state == 'open' and checkout.state != 'open':
                    vals['checkout_date'] = fields.Date.today()
                if new_state == 'done' and checkout.state != 'done':
                    vals['closed_date'] = fields.Date.today()
        result = super().write(vals)
        # Code after write: can use `self`, with the updated values
        return result

    @api.multi
    def button_done(self):
        done_stage = self.env['library.checkout.stage'].search([('state','=','done')], limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True

class CheckoutLine(models.Model):
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'

    checkout_id = fields.Many2one(comodel_name='library.checkout')
    book_id = fields.Many2one(comodel_name='library.book')