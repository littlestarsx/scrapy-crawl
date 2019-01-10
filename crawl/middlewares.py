# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.pipelines.images import ImagesPipeline
import random


class CrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        user_agent = ua.random
        print("当前用户代理>>" + user_agent + "<<")
        request.headers['User_Agent'] = user_agent


class CrawlProxyMiddleware(object):
    def process_request(self, request,  spider):
        PROXYPOOL = [
            {"ipaddr": "115.218.217.119:9000"},
            {"ipaddr": "144.255.12.232:9999"},
            {"ipaddr": "114.230.69.250:9999"},
            {"ipaddr": "111.177.181.223:9999"},
            {"ipaddr": "175.161.1.53:9000"}
        ]
        proxy = random.choice(PROXYPOOL)
        print("当前代理IP>>" + proxy["ipaddr"]) + "<<"
        request.meta["proxy"] = "http://%s" % proxy["ipaddr"]


class CrawlImagePipeline(ImagesPipeline):
    # 重载ImagePipeline中的item_completed方法，获取下载地址
    def item_completed(self, results, item, info):
        for ok,value in results:   #通过断点可以看到图片路径存在results内
            image_file_path= value['path'] #将路径保存在item中返回
            item['image_url_local'] = image_file_path
        return item