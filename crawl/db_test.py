#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crawl.mysql_obj import MysqlObj
from crawl.db_connect import connectRedis
from crawl.redis_queue import RedisQueue
from crawl.log import Log

fields = ['id,cat_id,title,content,dpi,is_subtitles,type,link_url,hits']
result = {}
mysqlObj = MysqlObj()
result = mysqlObj.select('article', fields=fields)
print(result)

#待处理队列
redisdb = connectRedis()
waitTaskQueue = RedisQueue('testlist')
task_info = '123'
waitTaskQueue.luaLPut(task_info)

#日志对象
log = Log()
log.addLog('测试日志','error:112233')



























