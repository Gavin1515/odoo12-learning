#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

{
    'name': 'Library Checkout',
    'description': 'Members can borrow books from the library.',
    'author': 'Gavin',
    'depends': ['library_member', 'mail'],
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'data/library_checkout_stage.xml',
        'views/library_menu.xml',
        'views/checkout_view.xml',
        'views/checkout_kanban_view.xml',
        'wizard/checkout_mass_message_wizard.xml',
    ],
}