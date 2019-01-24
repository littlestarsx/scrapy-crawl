# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CodecastsLaravelZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #索引（id方便视频排序）
    index = scrapy.Field()
    #标题
    title = scrapy.Field()
    #详情链接
    url = scrapy.Field()
    #视频名称
    video_name = scrapy.Field()
    #视频存储目录
    video_path = scrapy.Field()
    #视频请求referer(详情链接)
    video_referer = scrapy.Field()
    #视频播放下载链接
    video_url = scrapy.Field()
    headers = scrapy.Field()
    cookie = scrapy.Field()