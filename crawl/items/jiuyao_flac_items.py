# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiuyaoFlacItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #详情链接
    detail_url = scrapy.Field()
    #歌曲名称
    music_name = scrapy.Field()
    #歌曲存储目录
    music_path = scrapy.Field()
    #音乐播放下载链接
    music_url = scrapy.Field()
    headers = scrapy.Field()
    cookie = scrapy.Field()