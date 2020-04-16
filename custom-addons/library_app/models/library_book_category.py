#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import models, fields

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Book Category'
    '''
        注意这些附加操作会带来存储和执行速度的开销，所以最好是用到读的频率大于写的情况下，比如本例中的分类树。
        仅在优化多节点深度层级时才需要使用，对于小层级或浅层级的可能会被误用。
    '''

    # 使用该属性必须要添加且必须要索引parent_path字段
    _parent_store = True
    '''_parent_name属性： 
        如果模型中关联父模型的字段不是parent_id，那么可以通过_parent_name属性来指定关联父模型的字段。
        只要这些模型有parent_id字段（或_parent_name有效模型定义）就可以使用parent_of和child_of这些操作符。
    '''

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    parent_id = fields.Many2one(comodel_name="library.book.category", string="Parent Category", ondelete="restrict")
    # Optional but good to have:
    child_ids = fields.One2many(comodel_name="library.book.category", string="Subcategories", inverse_name="parent_id")
    # 和_parent_store模型属性配合使用，代替旧版本的parent_left和parent_right
    parent_path = fields.Char(index=True)

    # Reference Field:
    '''
        自odoo12开始，删除了可引用模型配置表。在此前版本中，可用于配置在 Reference 字段中可用的模型。
        通过菜单Settings > Technical > Database Structure可进行查看。
        这些配置可在 Reference 字段中使用odoo.addons.res.res_request.referenceable_models函数来替代模型选择列表。
        
        Reference字段的selection属性可以只当一个动态返回可变值集的列表。
        
        引用字段在数据库中以model,id字符串形式存储
        read()方法供外部应用使用，以格式化的('model_name',id)元组返回，而不是常用的many-to-one字段的(id,'display_name')形式
    '''
    highlighted_id = fields.Reference(selection=[('library.book','Book'), ('res.partner','Author')],
                                      string="Category HighLight")