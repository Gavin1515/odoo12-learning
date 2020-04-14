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
        'views/book_list_template.xml',
    ],
    # 数据文件会在模块升级时重新导入，但演示文件则并非如此，它们仅在安装时导入。
    # （但测试结果是删除升级会重建，升级不会更新演示数据）
    'demo': [
        # 注意初始化文件的加载顺序，被引用的必须先被初始化。
        # csv初始化文件，文件名必须和模型名对应上。
        'data/res.partner.csv',
        'data/library.book.csv',
        # 使用xml文件初始化数据时，文件名没有要求。
        'data/library_demo.xml',
    ]
}