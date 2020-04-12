#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

{
    'name': 'Library Members',
    'description': 'Manage people who will be able to borrow books.',
    'author': 'Gavin',
    # 继承mail模块以提供讨论和待办事项功能
    'depends': ['library_app', 'mail'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'security/library_security.xml',
        'views/book_view.xml',
        'views/library_menu.xml',
        'views/member_view.xml',
    ]
}