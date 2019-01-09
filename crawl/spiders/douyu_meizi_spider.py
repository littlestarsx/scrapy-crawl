# -*- coding: utf-8 -*-
import scrapy
import json
from crawl.items.douyu_meizi_items import DouyuMeiziItem


class DouyuMeiziSpiderSpider(scrapy.Spider):
    name = 'douyu_meizi_spider'
    allowed_domains = ['douyucdn.cn']
    offset = 0
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [base_url + str(offset), ]

    def parse(self, response):
        # 获取响应内容,字符串
        content = response.text
        data = json.loads(content)['data']

        for i in data:
            # 图片链接
            image_url = i['vertical_src']
            #item导入
            item = DouyuMeiziItem()
            # 该字段必须是图片链接的可迭代对象，否则报错
            item['image_urls'] = [image_url]
            yield item

        if self.offset < 230:
            self.offset += 20
            yield scrapy.Request(url=self.base_url + str(self.offset), callback=self.parse)