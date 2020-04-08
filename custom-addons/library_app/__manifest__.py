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
        'views/library_menu.xml',
    ]
}