#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields

class Member(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread','mail.activity.mixin']

    card_number = fields.Char(string='Card Number')
    '''
        delegate属性指定partner_id是一个用于代理继承的字段，他是odoo8子女增的特性，
        作用同_inherits = {‘res.partner’: ‘partner_id’}
        代理继承的特点：
        1.子模型继承了父模型的数据结构，但是子模型的数据库中除了本身的字段外，并不存储父模型的字段；
        2.子模型可以使用父模型的所有字段，但是不能使用父模型的方法（函数）
        
        代理继承可通过如下组合来进行替代：
            1.父模型中的一个 many-to-one 字段
            2.重载 create()方法自动创建并设置父级记录
            3.父字段中希望暴露的特定字段的关联字段
        有时这比完整的代理继承更为合适。例如res.company并没有继承res.partner，但使用到了其中好几个字段。
    '''
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner',
                                 delegate=True, ondelete='cascade', required=True)
