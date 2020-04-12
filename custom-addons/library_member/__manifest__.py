#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

{
    'name': 'Library Members',
    'description': 'Manage people who will be able to borrow books.',
    'author': 'Gavin',
    'depends': ['library_app'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'security/library_security.xml',
        'views/book_view.xml',
        'views/library_menu.xml',
        'views/member_view.xml',
    ]
}