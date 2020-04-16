#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from odoo import fields, models, api
from odoo.exceptions import Warning, ValidationError

class Book(models.Model):
    _name = 'library.book' # 仅有模型名使用点号(.) 来分割关键字，其它如模块、XML 标识符、数据表名等都使用下划线(_)
    _description = 'Book'
    _order = 'name,date_published desc'
    '''
        _name是我们创建的Odoo模型的内部标识符，在创建新模型时为必填。
        _description是对用户友好的模块记录标题，在用户界面中查看模型时显示。可选但推荐添加。
        _order设置浏览模型记录时或列表视图的默认排序。其值为SQL语句中orderby使用的字符串，所以可以传入符合SQL
            语法的任意值，它有智能模式并支持可翻译及many - to - one字段名。
        _rec_name在从关联字段（如many-to-one关联）中引用时作为记录描述。
            默认使用模型中常用的 name字段，但可以指定任意其它字段。
        _table是模型对应的数据表名。默认表名由 ORM 通过替换模块名中的点为下划线来自动定义，但是可通过该属性指定表名。
        _log_access=False用于设置不自动创建审计追踪字段：create_uid, create_date, write_uid和write_date。
        _auto=False 用于设置不自动创建模型对应的数据表。如有需要，可通过重载init()方法来创建数据库对象：数据表或视图。
    '''
    # String Fileds
    '''
        文本字符串：Char, Text和Html有一些特有属性：
        size (Char)设置最大允许尺寸。无特殊原因建议不要使用，例如可用于带有最大允许长度的社保账号。
        translate  使用得字段内容可翻译，带有针对不同语言的不同值。
        trim  默认值为 True，启动在网络客户端中自动去除周围的空格。可通过设置trim=false来取消。
              trim字段属性在 Odoo 12中引入，此前版本中文本字段保存前后的空格。
    '''
    name = fields.Char(string="Title", default=None,
                       index=True, help='Book cover title',
                       readonly=False, required=True, translate=False)
    isbn = fields.Char(string='ISBN')
    # 元组第一个元素是存储在数据库中的值，第二个元素是展示在用户界面中的描述。
    # 该列表可由其它模块使用selection_add关键字参数扩展。
    book_type = fields.Selection(string="Type", selection=[
        ('paper', 'Paperback'),
        ('hard', 'Hardcover'),
        ('electronic', 'Electronic'),
        ('other', 'Other')])
    notes = fields.Text(string="Internal Notes")
    # 出于安全考虑，Html字段会被清洗，但清洗行为可被重载。
    descr = fields.Html(string="Description")
    # Numberic Fields
    copies = fields.Integer(default=1)
    avg_rating = fields.Float(string="Average Rating", digits=(3,2))
    price = fields.Monetary(string="Price", currency_field="currency_id")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency") # price helper
    # Date and Datetime Fields
    # 从Odoo12开始，Date和Datetime 字段现在 ORM 中作为日期对象处理。
    # 此前的版本中作为文本字符串处理，进行操作时需与 Python 日期对象间进行转换。
    date_published = fields.Date()
    last_borrow_date = fields.Datetime(string="Last Borrowed On", default=lambda self: fields.Datetime.now())
    # Other Fields
    '''
        active (Boolean型)允许我们关闭记录。带有active=False的记录会自动从查询中排除掉。
        可在当前上下文中添加{‘active_test’: False} 来关闭这一自动过滤。可用作记录存档或假删除（soft delete）
        例如：
            >>> self.env['library.book'].search([])
            library.book(3, 1)
            >>> self.env['library.book'].with_context(active_test=False).search([])
            library.book(3, 2, 1)
    '''
    active = fields.Boolean(string='Active?', default=True)
    image = fields.Binary(string='Cover')

    '''字段属性：
            readonly=True 会使用户界面中的字段默认不可编辑。
                在API层面并没有强制，模型方法中的代码仍然可以向其写入。仅针对用户界面设置。
            groups 可限制字段仅对一些组可访问并可见。
                值为逗号分隔的安全组XML ID列表，如groups='base.group_user,base.group_system'。
            states传入依赖 state字段值的 UI 属性的字典映射值。可用属性有readonly, required和invisible，
                例如states={‘done’:[(‘readonly’,True)]}。注意states 字段等价于视图中的 attrs 属性。
                同时注意视图也支持 states 属性，但用途不同，传入逗号分隔的状态列表来控制元素什么时候可见。
            当模块数据结构在不同版本中变更时以下两个属性非常有用：
            deprecated=True在字段被使用时记录一条 warning 日志
            oldname=’field’是在新版本中重命名字段时使用，可在升级模块时将老字段中的数据自动拷贝到新字段中
        '''

    '''
        parent_id和parent_path Integer和Char型)对于父子层级关系具有特殊意义。
        从Odoo12开始 层级关联现在使用parent_path字段，它替代了老版本中已淘汰的parent_left和 parent_right字段(整型)。
    '''

    # Relational Fields
    publisher_id = fields.Many2one(comodel_name='res.partner', string='Publisher')
    author_ids = fields.Many2many(comodel_name='res.partner', string="Authors")
    '''Many2one字段属性：
        auto_join=True 允许ORM在使用关联进行搜索时使用SQL连接。
            使用时会跳过访问安全规则，用户可以访问安全规则不允许其访问的关联记录，但这样 SQL 的查询会更有效率且更快。
        测试auto_join属性: 针对代码：self.search([('publisher_id.name', '=', 'Daniel Reis')])
            在publisher_id字段上添加auto_join属性之前的查询SQL：
            SELECT "res_partner".id FROM "res_partner" WHERE ("res_partner"."name" = 'Daniel Reis') AND (("res_partner"."type" != 'private')  OR  "res_partner"."type" IS NULL ) ORDER BY "res_partner"."display_name"
            SELECT "library_book".id FROM "library_book" WHERE (("library_book"."active" = true)  AND  ("library_book"."publisher_id" in (44))) AND ("library_book"."active" = true) ORDER BY "library_book"."name" ,"library_book"."date_published" DESC
            在publisher_id字段上添加auto_join属性之后的查询SQL：
            SELECT "library_book".id FROM "res_partner" as "library_book__publisher_id","library_book" WHERE ("library_book"."publisher_id"="library_book__publisher_id"."id") AND (("library_book"."active" = true)  AND  
            ("library_book__publisher_id"."name" = 'Daniel Reis')) AND ("library_book"."active" = true) ORDER BY "library_book"."name" ,"library_book"."date_published" DESC
        
        delegate=True 创建一个关联记录的代理继承。使用时必须设置required=True和ondelete=’cascade’。
    '''

    # Compute Field:
    '''
        方法名作为字符串参数传入字段中，但也可以传递一个可调用引用(方法标识符，不带引号)。
        但这时需确定Python 文件中方法在字段之前定义。
    '''
    publisher_country_id = fields.Many2one(comodel_name="res.country", string="Publisher Country",
                                           compute="_compute_publisher_country",
                                           inverse="_inverse_publisher_country",
                                           search="_search_publisher_country")
    # 其实@api.depends只有在计算字段存储数据库时有效。
    # 不存储就是打开计算字段所在视图时触发实时计算，并不会在依赖字段变化时才触发。
    @api.depends('publisher_id.country_id')
    def _compute_publisher_country(self):
        # 计算函数必须为一个或多个字段分配值用于计算。
        # 如果计算方法有 if 条件分支，确保每个分支中为计算字段分配了值。否则在未分配置值的分支中将会报错。
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    '''
        计算字段中的写入是计算的反向(inverse)逻辑。因此处理写入操作的方法称为 inverse，本例中 inverse 方法很简单。
        计算将book.publisher_id.country_id 的值复制给book.publisher_country_id，
        反向操作是将写入book.publisher_country_id的值拷贝给book.publisher_id.country_id field字段
    '''
    def _inverse_publisher_country(self):
        for book in self:
            book.publisher_id.country_id = book.publisher_country_id

    # 要为计算字段开启搜索操作，需要实现search 方法。为此我们需要能够将计算字段的搜索转换为使用常规存储字段的搜索域。
    def _search_publisher_country(self, operator, value):
        return [('publisher_id.country_id', operator, value)]

    # related filed:
    '''
        本质上关联字段仅仅是快捷实现search和inverse方法的计算字段。也就是说可以直接对其进行搜索和写入，而无需书写额外的代码。
        默认关联字段是只读的，因inverse写操作不可用，可通过readonly=False字段属性来开启写操作。
        
        Odoo 12中的修改: 现在关联字段默认为只读：readonly=True。
        此前版本中它默认可写，但事实证明这是一个默认值，因为它可能会允许修改配置或主数据这些不应被修改的数据。
    '''
    # publisher_country_id = fields.Many2one(comodel_name="res.country", string="Publisher Country",
    #                                        related='publisher_id.country_id')

    # SQL约束
    _sql_constraints = [
        ('library_book_name_date_uq',  # 约束唯一标识符
         'UNIQUE (name, date_published)',  # 约束 SQL 语法
         'Book title and publication date must be unique'),  # 消息
        ('library_book_check_date',
         'CHECK (date_published <= current_date)',
         'Publication date must not be in the future.'),
    ]

    # Python约束
    @api.constrains('isbn')
    def _constrain_isbn_valid(self):
        for book in self:
            if book.isbn and not self._check_isbn():
                raise ValidationError('%s is an invalid ISBN' % book.isbn)

    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        isbn = self.isbn.replace('-', '')
        digits = [int(x) for x in isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi
    def action_check_isbn(self):
        print("fdsvf")
        for book in self:
            if not book.isbn:
                raise Warning("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
            return True
