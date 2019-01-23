# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CodecastsLaravelZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    video_name = scrapy.Field()
    video_path = scrapy.Field()
    video_referer = scrapy.Field()
    video_url = scrapy.Field()
    headers = scrapy.Field()
    cookie = scrapy.Field()