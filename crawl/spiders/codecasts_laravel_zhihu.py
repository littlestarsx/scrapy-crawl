# -*- coding: utf-8 -*-
import scrapy
from crawl.items.codecasts_laravel_zhihu_items import CodecastsLaravelZhihuItem
import os


class CodecastsLaravelZhihuSpider(scrapy.Spider):
    #爬虫名字
    name = 'codecasts_laravel_zhihu_spider'
    #允许域名
    allowed_domains = ['www.codecasts.com']
    #入口url，扔到调度器中
    start_urls = ['https://www.codecasts.com/series/build-a-zhihu-website-with-laravel']

    #默认解析方法
    def parse(self, response):
        video_list = response.css("tbody tr.episode-wrap")
        for i_item in video_list:
            #item文件导入
            item = CodecastsLaravelZhihuItem()
            #数据解析
            cookie = {
                '__asc' : '9f88351216878b6708f1850f102',
                '__auc' :'9f88351216878b6708f1850f102',
                'Hm_lvt_5d92f95c051389a923e14e448ede2cf4' : '1548213498, 1548213501, 1548213639, 1548213663',
                'Hm_lpvt_5d92f95c051389a923e14e448ede2cf4' : '1548213663',
                'laravel_session' : 'eyJpdiI6IjhFYWpUVjVRR2lEdnVxR1B5bjUzNWc9PSIsInZhbHVlIjoiQkN4Q01BalFwVURXXC9MUUl5XC9OZGJEZitsNTQyQ3lxK3R3QjBwQldtUEowSkJITGQ3TXNycVJrQlRmRksxVTQyQmtWek1nMlAwM3dTcTkxV01ZcVN1UT09IiwibWFjIjoiZTMzYmRkNTdkMmNlYTJmNDBiOTAxMmE2YzY0NjMzNDM2ODA2ZDQ5MTNiYTM0Y2Q3YmRkM2FlY2MwZmU4Y2ZhYiJ9'
            }
            headers = {
                'referer': self.start_urls[0],
            }

            index = i_item.css("td.episode-index::text").extract_first()
            index_text = index.strip()
            item['index'] = index_text
            title = i_item.css("td.episode-title>a>span::text").extract_first()
            item['title'] = title
            url = i_item.css("td.episode-title>a::attr(href)").extract_first()
            item['url'] = url
            item['video_name'] = index_text + '-' + title + '.mp4'
            item['video_path'] = os.getcwd() + '/video/codecasts/laravel-zhihu/'
            item['video_referer'] = url
            item['headers'] = {
                'referer': url
            }
            item['cookie'] = cookie
            yield item
            #meta传item字典一起yield
            yield scrapy.Request(url=url, callback=self.video_parse, headers=headers, cookies=cookie, meta={'item': item})


    #获取视频链接一起yield
    def video_parse(self, response):
        video_url = response.css("div.container video>source::attr(src)").extract_first()
        item = response.meta['item']
        item['video_url'] = video_url
        # 将数据yield到pipelines下载视频
        yield item