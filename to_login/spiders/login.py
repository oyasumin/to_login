# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile?_next=/places/default/index']

    def parse(self, response):
        # 解析登录后下载的页面，此例中为用户个人信息页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        yield dict(zip(keys, values))

    # 登录
    # 登录页面url
    login_url = 'http://example.webscraping.com/places/default/user/login'

    # 覆写基类的start_requests方法，最先请求登录页面
    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    # login方法为登录页面的解析函数，在该方法中进行模拟登录，构造表单并提交
    def login(self, response):
        # 登录页面的解析函数，构造FormRequest对象提交表单
        fd = {'email':'sherby@gmail.com', 'password':'tomsherby'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    # parse_login方法为表单请求的响应处理函数。
    # 通过在页面查找特殊字符串'Welcome sherby'。如果登录成功，调用基类的start_requests方法继续爬取start_urls中的页面
    def parse_login(self, response):
        # 登录成功后，继续爬取start_urls中的页面信息
        if 'Welcome sherby' in response.text:
            # yield理解成“返回”，yield from理解成“从什么(生成器)里面返回”
            # python3语法调用基类的start_requests()方法
            yield from super().start_requests()
