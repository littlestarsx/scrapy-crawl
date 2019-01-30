# -*- coding: utf-8 -*-
import scrapy
from crawl.items.jiuyao_flac_items import JiuyaoFlacItem
import os
import json

#〖普通用户〗每天只能使用 3 次128MP3下载服务，如需解除限制，请 开通会员。
class JiuyaoFlacSpider(scrapy.Spider):
    #爬虫名字
    name = 'jiuyao_flac_spider'
    #允许域名
    allowed_domains = ['www.91flac.com']
    #入口url，扔到调度器中
    start_urls = [
        'https://www.91flac.com/playlists/857253',#200首华语金曲，你一定在KTV点过这些歌 精选歌单 曲目列表
        # 'https://www.91flac.com/playlists/2351201',#KTV麦霸必修华语金曲100首 精选歌单 曲目列表
        # 'https://www.91flac.com/playlists/4149582',#全民K歌翻唱热歌榜盘点 精选歌单 曲目列表
        # 'https://www.91flac.com/playlists/3705285',#2018年抖音最火背景乐精选集 精选歌单 曲目列表
    ]

    #默认解析方法
    def parse(self, response):
        music_list = response.css("div.table-responsive tbody tr")
        for i_item in music_list:
            #item文件导入
            item = JiuyaoFlacItem()
            #数据解析
            detail_url = i_item.css("td:nth-child(1)>a::attr(href)").extract_first()
            item['detail_url'] = detail_url
            music_name = i_item.css("td:nth-child(1)>a::text").extract_first()
            singer = i_item.css("td:nth-child(2)>a::text").extract_first()
            item['music_name'] = music_name + '-' + singer + '.mp3'
            item['music_path'] = os.getcwd() + '/music/91flac/playlists/'
            headers = {
                'pragma': 'no-cache',
                'referer': detail_url,
                'x-csrf-token': 'DLjJo2lnHJf9DN5RXUohgw1Y0B7PjtUHWrsWcEmU',
                'x-xsrf-token': 'eyJpdiI6InpCQVpEY3UwaDVla2NPNmd6eTJcL05nPT0iLCJ2YWx1ZSI6Ik0wZkVIVGU5NjNMWkVSeGZPYTdkMHRXbEZmTit0OHh2QjZHT3RQVlwvNW5OOVErMlwvYzRMMWhUdERnaytxUGVjViIsIm1hYyI6ImYxMzFlMTg4NWRjYTc3YzlmZGZmMDlkMDdkMDI3MWUwYWFjNmE4Mjc2MmIxMTFmMDdjMGYyNzIyMTRjYjZhYjYifQ=='
            }
            item['headers'] = headers
            cookie = {
                'XSRF-TOKEN': 'eyJpdiI6IkZtQitBT2RlSWpjV0hRRWY0V3dxWXc9PSIsInZhbHVlIjoiQUJZZkdIclI4cmE3VzdTZTBPMDQxeDJnejU1a1wvUE1DeGF3YmRCWnIxcWlhaXVaVEN6emFoNEM1VmV3anphMHgiLCJtYWMiOiJmNGZmNTAxN2Y3ZTg1NDg1ZWNiNzYwYWRiZjc2ZDI3ZDg4MGMxYTgzOTJkZDBmYzJhZmZkZjMyY2NiMjdiMmZlIn0%3D',
                '91flac_session': 'eyJpdiI6ImVVdHJsc0tFTERST2daeTIwMndtaGc9PSIsInZhbHVlIjoieU1wQmN2enJrcEV2NWFDeFBhWWU1Y0ZBRDdSd0JYTDBBdGNzR2VrVlFcL2pyYmJZK2psUzBPZTB2MzJmUWZDS3EiLCJtYWMiOiI2MTBmZTcxYmFiOWUwNTllOWQ3MGIwZmU3Nzk1MDMxYjViNGM4NjA2MjFlM2Y5MDk4N2VlZGJhNjQxZGMzNTEyIn0%3D'
            }
            item['cookie'] = cookie
            #meta传item字典一起yield
            api_url = detail_url + '/link'
            yield scrapy.Request(url=api_url, callback=self.music_parse, method='POST', headers=headers, cookies=cookie, meta={'item': item})


    #获取音乐链接一起yield
    def music_parse(self, response):
        item = response.meta['item']
        response_json = json.loads(response.text)
        music_url = response_json['128mp3']
        print(music_url)
        music_download_url = str(music_url) + '&from=download'
        print(music_download_url)
        item['music_url'] = music_download_url
        # 将数据yield到pipelines下载音乐
        yield item