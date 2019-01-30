#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@author:
@file: codecasts_laravel_zhihu_pipelines.py
@time: 2019/1/4
@desc:
'''
import requests
import os


class JiuyaoFlacPipeline(object):
    def process_item(self, item, spider):
        #保存视频
        music_url = item['music_url']
        music_name = item['music_name']
        music_path = item['music_path']
        headers = item['headers']
        cookie = item['cookie']
        resp = requests.get(url=music_url, headers=headers, cookies=cookie)
        #视频是二进制数据流，content就是为了获取二进制数据的方法
        data = resp.content
        #创建路径
        self.make_dir(music_path)
        f = open(music_path + music_name, 'wb')
        f.write(data)
        f.close()
        print('下载完成')
        return item


    #检测目录创建目录
    def make_dir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

