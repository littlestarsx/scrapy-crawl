#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys,re 
import datetime

class Log(object):

    def __init__(self):
        #self.rootDir = os.getcwd()
        self.logRootDir= os.path.split( os.path.realpath( sys.argv[0] ) )[0]
        
    #记录日志
    #status 日志类型 process(过程日志)，error(错误日志) success(成功日志)
    def addLog(self,  log_contxt, status ='process'):
        
        try:
            logDir = self.logRootDir + '/logs/'
            folder = os.path.exists(logDir)  
            if not folder: 
                os.makedirs(logDir)

            #定义日志文件
            if status == 'error':
                fileName = self.logRootDir+'/logs/error_log.txt'
            else :
                fileName = self.logRootDir+'/logs/process_log.txt'

            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
            f = open(fileName, 'a')
            f.write(nowTime + ':' + log_contxt+'\n')
            f.close()

            return True
        except Exception as err:
            print (1,err) 

                  
        
