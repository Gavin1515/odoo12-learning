#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models,fields,api

class CheckoutMassMessage(models.TransientModel):
    _name = 'library.checkout.massmessage'
    _description = 'Send Message to Borrowers'

    '''
        值得注意的是普通模型中的one-to-many关联不能在临时模型中使用。
        这是因为那样就会要求普通模型中添加与临时模型的反向many-to-one关联。
        但这是不允许的，因为那样普通记录的已有引用会阻止对老的临时记录的清除。替代方案是使用many-to-many关联。
        Many-to-many关联存储在独立的表中，会在关联任意一方被删除时自动删除表中对应行。
    '''
    checkout_ids = fields.Many2many(comodel_name='library.checkout', string='Checkouts')
    message_subject = fields.Char()
    message_body = fields.Html()

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['checkout_ids'] = self.env.context.get('active_ids')
        return defaults

    @api.multi
    def button_send(self):
        self.ensure_one()
        for checkout in self.checkout_ids:
            checkout.message_post(subject=self.message_subject, body=self.message_body,
                                  subtype="mail.mt_comment")
        '''
            让方法至少返回一个 True 值是一个很好的编程实践。
            主要是因为有些XML-RPC协议不支持 None 值，所以对于这些协议就用不了那些方法了。
            在实际工作中，我们可能不会遇到这个问题，因为网页客户端使用JSON-RPC而不是XML-RPC，但这仍是一个可遵循的良好实践。
        '''
        return True