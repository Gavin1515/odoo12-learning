# odoo12-learning
odoo12 development learning from https://alanhou.org/odoo-12-development/

## 修改记录集执行环境
记录集执行环境是不可变的，因此不能被修改，但我们可以创建一个变更环境并使用它来执行操作。我们通过如下方法来实现：<br>
<code>env.sudo(user)</code>：中传入一条用户记录并返回该用户的环境。如未传入用户，则使用__system__超级用户root，这时可绕过安全规则执行指定操作。<br>
<code>env.with_context(<dictionary>)</code>： 替换原上下文为新的上下文<br>
<code>env.with_context(key=value,…)</code>：修改当前上下文，为一些键设置值<br>

## 针对Odoo域其实有两种运行上下文：
1.在窗口操作或字段属性等客户端中使用时，可使用原生字段值来渲染当前可用视图，但不能对其使用点标记符。
2.在服务端使用时，如安全记录规则或服务端 Python 代码中，可以对字段使用点标记符，因为当前记录是一个对象

## Odoo 12中的修改
odoo12中date和datetime字段值以 Python 对象表示，而此前 Odoo 版本中它们以文本字符串表示。这些字段类型值仍可像此前 Odoo 版本中那样使用文本表示。

## 日期和时间
1.odoo的fields.Date和fields.Datetime封装了一些工具方法处理日期和函数，但是格式仅限于如下格式：<br>
odoo.tools.DEFAULT_SERVER_DATE_FORMAT<br>
odoo.tools.DEFAULT_SERVER_DATETIME_FORMAT<br>
它们分别与%Y-%m-%d和%Y-%m-%d %H:%M:%S相对应<br>
2.对于其它的日期和时间格式，可使用Python datetime模块中的strptime和strftime方法


## Odoo中执行SQL
self.env.cr.execute(SQL, Parames)
还可以使用数据操纵语言(DML) 来运行指令，如UPDATE和INSERT。因为服务器保留数据缓存，这可能导致与数据库中实际数据的不一致。<br>
出于这个原因，在使用原生DML后，应使用self.env.cache.invalidate()清除缓存。

## Odoo装饰器
1.如果模型方法没有添加装饰器，默认就使用@api.multi。<br>
2.@api.one的返回值有些搞怪，它返回一个列表，而不实际方法返回的数据结构。比如方法代码如果返回字典，实际返回值是一个字典值列表。<br>
这种误导性也是该方法被弃用的主要原因。<br>
3.@api.model装饰的方法无法用于用户界面按钮，在这种情况下，应使用@api.multi。<br>
4.通过为字段添加属性on_change=”0″可在特定表单中关闭 on change 行为，比如<field name=”fld1″ on_change=”0″ />

## ORM方法
1.Odoo 12中的修改：create()现在也可批量创建数据，这通过把单个字典对象修改为字典对象列表来传参进行实现。
这由带有@api.model_create_multi装饰器的create() 方法来进行支持。
2.name_create(name)创建一条仅带有要使用的标题名的新记录。它用于在 UI 中快速创建(quick-create)功能，
这里我们可以仅提供名称快速创建一条关联记录。可扩展来为通过此功能创建的新记录提供指定默认值。