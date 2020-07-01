{
    'name': 'Library Management',
    'description': 'Manage library book catalogue and lending.',
    'author': 'Gavin',
    'depends': ['base'],
    'application': True,
    'data':[
        # 注意library_security.xml 加在library_menu.xml文件之前，数据文件的加载顺序非常重要，因为我们只能引用已经定义过的标识符。
        # 菜单项经常引用到安全组，所以建议将安全组定义文件放到菜单和视图文件之前。
        'security/library_security.xml',
        # csv文件的文件名必须和要导入的目标模型名一致（除了.csv后缀）
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/book_view.xml',
        'views/book_list_template.xml',
        'reports/library_book_report.xml',
        'reports/library_book_sql_report.xml',
    ]
}
