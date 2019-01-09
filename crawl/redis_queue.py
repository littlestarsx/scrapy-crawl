#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import redis
import time

import crawl.db_connect as connect_obj

#lua 去重脚本，增加set集合，根据集合去重
SCRIPT_RPUSH = '''
local q = KEYS[1]
local q_set = KEYS[1] .. "_set"
local v = redis.call("SADD", q_set, ARGV[1])
if v == 1
then
    return redis.call("RPUSH", q, ARGV[1]) and 1
else
    return 0
end
'''

#LPUSH
SCRIPT_LPUSH = '''
local q = KEYS[1]
local q_set = KEYS[1] .. "_set"
local v = redis.call("SADD", q_set, ARGV[1])
if v == 1
then
    return redis.call("LPUSH", q, ARGV[1]) and 1
else
    return 0
end
'''

#单独pop队列及删除set集合内容
SCRIPT_POP = '''
local q = KEYS[1]
local q_set = KEYS[1] .. "_set"
local v = redis.call("LPOP", q)
if v ~= ""
then
    redis.call("SREM", q_set, v)
end
return v
'''

#移除列表中与参数 value 相等的元素。
SCRIPT_LREM = '''
local q = KEYS[1]
local q_set = KEYS[2] .. "_set"
local v = redis.call("LREM", q,  0, ARGV[1])
if v ~= ""
then
    redis.call("SREM", q_set, ARGV[1])
end
return v
'''


class RedisQueue(object):

    def __init__(self, name, namespace='PYTHON_VIDEO'):

        self.__db = connect_obj.connectRedis()
        
        self.__namespace = namespace
        self.__name = name
        self.key = '%s:%s' %(namespace, name)

        #注册lua脚本
        self.rpushScript = self.__db.register_script(SCRIPT_RPUSH)
        self.lpushScript = self.__db.register_script(SCRIPT_LPUSH)
        self.popScript  = self.__db.register_script(SCRIPT_POP)
        self.lremScript = self.__db.register_script(SCRIPT_LREM)
    
    # 返回队列里面list内元素的数量
    def qsize(self):
        return self.__db.llen(self.key)

    def put(self,item):
        return self.__db.rpush(self.key,item)
    
    def pop(self,item):
        return self.__db.pop(self.key)
           
    #写入队列 加入set集合去重复值
    def luaRPut(self, item):
        return self.rpushScript( keys=[self.key], args = [item,0] )
    
    #写入队列 加入set集合去重复值
    def luaLPut(self, item):
        return self.lpushScript( keys=[self.key], args = [item,0] )

    #普通弹出队列，删除set集合值
    def luaPop(self):
        return self.popScript( keys=[self.key], args = [] )

    #移除列表中与参数 item 相等的（所有）元素。
    def luaLrem(self, item):
        queuename = '%s:%s–%s' %(self.__namespace, self.__name , 'tmp_task')
        item = self.lremScript(keys=[queuename,self.key], args = [item,0])
        return item

    def lrem(self, item):
        item = self.__db.lrem(self.key,item,0)
        return item

    #BRPOPLPUSH source destination timeout
    # **安全队列 （阻塞模式）**
    # 注意：消费队列时，同时原子性操作放入临时队列，防止程序意外退出消息丢失
    def rpoplpushWait(self, timeout=None):

        queuename = '%s:%s–%s' %(self.__namespace, self.__name , 'tmp_task')
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.brpoplpush(self.key, tmpqueue, timeout=timeout)
        if item:
            item = item[1]  # 返回值为一个tuple
        return item

    #将 source 弹出的元素插入到列表 destination ，作为 destination 列表的的头元素。
    # **安全队列 （非阻塞模式） **
    # 注意：消费队列时，同时原子性操作放入临时队列，防止程序意外退出消息丢失
    def rpoplpush(self):
       
        queuename = '%s:%s–%s' %(self.__namespace, self.__name , 'tmp_task')
        # 将 source 弹出的元素插入到列表 destination ，作为 destination 列表的的头元素。
        item = self.__db.rpoplpush(self.key, queuename)  
        return item

