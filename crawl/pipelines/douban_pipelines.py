#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@author:
@file: douban_pipelines.py
@time: 2019/1/4
@desc:j
'''
from crawl.mysql_obj import MysqlObj


class DoubanPipeline(object):
    def process_item(self, item, spider):
        data = dict(item)
        mysqlObj = MysqlObj()
        result = mysqlObj.insert('movie', data)
        print(result)
        return item