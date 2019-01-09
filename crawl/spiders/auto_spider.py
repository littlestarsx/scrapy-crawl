# -*- coding: utf-8 -*-
import scrapy


class AutoSpiderSpider(scrapy.Spider):
    name = 'auto_spider'
    allowed_domains = ['www.autohome.com.cn']
    start_urls = ['http://www.autohome.com.cn/']

    def parse(self, response):
        pass
