#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo.tests.common import TransactionCase
from odoo import exceptions

'''
TransactionCase测试为每个测试使用不同的事务，在测试结束时自动回滚。
SingleTransactionCase将所有测试放在一个事务中运行，在最后一条测试结束后才进行回滚。
    在每条测试的最终状态需作为下一条测试的初始状态时这会非常有用。
'''
class TestWizard(TransactionCase):
    '''setUp()方法用于准备数据以及待使用的变量。通常我们将数据和变量存放在类属性中，这样就可在测试方法中进行使用。'''
    def setUp(self, *args, **kwargs):
        super(TestWizard, self).setUp(*args, **kwargs)
        # Setup test data
        admin_user = self.env.ref('base.user_admin')
        self.Checkout = self.env['library.checkout'].sudo(admin_user)
        self.Wizard = self.env['library.checkout.massmessage'].sudo(admin_user)

        a_member = self.env['library.member'].create({'name': 'John'})
        self.checkout0 = self.Checkout.create({'member_id': a_member.id})
    '''
        测试用例方法名必须以test_为前缀。这些方法被自动发现，该前缀就是用于辨别是否为实施测试用例的方法。
        根据测试方法名的顺序来运行。
        
        如果使用workers参数开启多线程的话，会出现如下测试失败的警告：
        WARNING ? odoo.service.server: Unit testing in workers mode could fail; use --workers 0.
    '''
    def test_button_send(self):
        # Send button should create messages on Checkouts
        msgs_before = len(self.checkout0.message_ids)

        wizard0 = self.Wizard.with_context(active_ids=self.checkout0.ids)
        wizard0 = wizard0.create({'message_body': 'Hello'})
        wizard0.button_send()

        msgs_after = len(self.checkout0.message_ids)
        # 如果断言执行失败会打印出第三个参数的信息
        self.assertEqual(msgs_before+1, msgs_after, 'Expected on additional message in the Checkout.')

    def test_button_send_empty_body(self):
        # 由于TransactionCase中每个test方法执行后都会回滚，因此上下文也被清空了
        wizard0 = self.Wizard.create({})
        # 要检查是否抛出异常，我们将相应代码放在self.assertRaises()代码块中。
        with self.assertRaises(exceptions.UserError) as e:
            wizard0.button_send()