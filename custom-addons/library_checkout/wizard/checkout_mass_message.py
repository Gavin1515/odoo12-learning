#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models,fields,api,exceptions
import logging
_logger = logging.getLogger(__name__)

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
        if not self.checkout_ids:
            '''Odoo 9中的修改: 引用了UserError异常来替换掉Warning异常，
                淘汰掉 Warning 异常的原因是因为它与 Python 内置异常冲突，但 Odoo 保留了它以保持向后兼容性。
            '''
            raise exceptions.UserError('请至少选择一条借阅记录来发送消息!')
        if not self.message_body:
            raise exceptions.UserError('请填写要发送的消息体!')

        for checkout in self.checkout_ids:
            checkout.message_post(subject=self.message_subject, body=self.message_body,
                                  subtype="mail.mt_comment")

        '''
            注意我们没有在日志消息中使用 Python 内插字符串。我们没使用_logger.info(‘Hello %s’ % ‘World’)，
            而是使用了类似_logger.info(‘Hello %s’, ‘World’)。不使用内插使我们的代码少执行一个任务，让日志记录更为高效。
            因此我们应一直为额外的日志参数传入变量。
            
            服务器日志的时间戳总是使用 UTC 时间。因此打印的日志消息中也是 UTC 时间。
            你可能会觉得意外 ，但 Odoo服务内部都是使用 UTC 来处理日期的.
            
            Odoo日志级别默认是info，而且可以通过命令行参数--loghandler=模块全路径:日志级别 来设置模块的日志级别。
        '''
        _logger.info('Send %d message to %s', len(self.checkout_ids), str(self.checkout_ids))
        '''
            让方法至少返回一个 True 值是一个很好的编程实践。
            主要是因为有些XML-RPC协议不支持 None 值，所以对于这些协议就用不了那些方法了。
            在实际工作中，我们可能不会遇到这个问题，因为网页客户端使用JSON-RPC而不是XML-RPC，但这仍是一个可遵循的良好实践。
            开启测试仅需在安装或升级(-i或-u)模块时在 Odoo 服务启动命令中添加– test-enable选项即可。
        '''
        return True