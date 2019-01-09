# -*- coding: utf-8 -*-
import scrapy
from crawl.items.douban_items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名字
    name = 'douban_spider'
    #允许域名
    allowed_domains = ['movie.douban.com']
    #入口url，扔到调度器中
    start_urls = ['https://movie.douban.com/top250']

    #默认解析方法
    def parse(self, response):
        #循环电影条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            #item文件导入
            douban_item = DoubanItem()
            #详细xpath,数据解析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//div[@class='pic']//em//text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='hd']//a//span[1]//text()").extract_first()
            content = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p[1]//text()").extract()
            #数据处理
            contents = ''
            for i_content in content:
                contents += "".join(i_content.split())
            douban_item['introduce'] = contents
            douban_item['star'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[@class='rating_num']//text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[4]//text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p[@class='quote']//span[@class='inq']//text()").extract_first()
            douban_item['image_url'] = i_item.css(".item .pic a img::attr(src)").extract_first()
            #将数据yield到pipelines里去
            yield douban_item
        # 解析下一页规则，取后一页xpath
        next_link = response.xpath("//span[@class='next']//link//@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)