#!/usr/bin/python3
# -*- coding: utf-8 -*-
import redis
import pymysql
import crawl.config_read as config_obj

def connectMysql():
    try:
        host = config_obj.getConfig('mysqlbase','dbhost')
        dbuser = config_obj.getConfig('mysqlbase', 'dbuser')
        dbpwd = config_obj.getConfig('mysqlbase', 'dbpassword')
        port = int(config_obj.getConfig('mysqlbase','dbport'))
        dbname = config_obj.getConfig('mysqlbase','dbname')
        dbcharset = config_obj.getConfig('mysqlbase','dbcharset')
        
        db = pymysql.connect(host=host, user=dbuser, passwd=dbpwd, port=port, db=dbname, charset=dbcharset, autocommit = True, cursorclass = pymysql.cursors.DictCursor )
        return db
    except Exception as e:
        print ('Mysql 数据库连接失败配置文件',e)
        return False


def connectRedis():
    try:
        host = config_obj.getConfig('redisbase','dbhost')
        port = config_obj.getConfig('redisbase','dbport')
        dbname = config_obj.getConfig('redisbase','dbname')
        dbauth = config_obj.getConfig('redisbase','dbpassword')
        pool = redis.ConnectionPool(host=host, port=port, db=dbname, password=dbauth)
        db = redis.Redis(connection_pool=pool)
        return db
    except Exception as e:
        print ('Redis 数据库连接失败配置文件', e)
        return False

