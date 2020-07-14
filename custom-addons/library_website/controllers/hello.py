# -*- coding:utf-8 -*-
from odoo import http

class Hello(http.Controller):

    # auth=’public’参数实际表示如果访客未登录则使用public特殊用户运行网页控制器。如果登录了，则使用登录用户来代替public。
    '''集成website模块并非严格要求website = True参数，不添加它也可以在模板视图中添加网站布局。但是通过添加可以让我们在网页控制器中使用一些功能：
        1.路由会自动变成支持多语言并且会从网站安装的语言中自动检测最接近的语言。需要说明这可能会导致重新路由和重定向。
        2.控制器抛出的任何异常都会由网站代码进行处理，这会将默认的错误码变成更友好的错误页面向访客展示。
        3.带有当前网站浏览记录的request.website变量，可在请求中进行使用。
        4.auth = public路由的public用户将是由后台网站配置中选择的用户。这可能会和本地区、时区等相关。
    如果在网页控制器中无需使用上述功能，则可省略website = True参数。
    但大多数网站QWeb模板需要使用website = True开启一些数据，比如底部公司信息，所以最好还是添加上。
    '''
    @http.route('/helloworld', auth='public', website=True)
    def helloworld(self, **kwargs):
        return http.request.render('library_website.helloworld')

    # 通过/hellocms/library_website.helloworld来调用
    @http.route('/hellocms/<page>', auth='public')
    def hello(self, page, **kwargs):
        return http.request.render(page)