#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@author:
@file: douban_pipelines.py
@time: 2019/1/4
@desc:
'''

class AutoPipeline(object):
    def process_item(self, item, spider):
        return item