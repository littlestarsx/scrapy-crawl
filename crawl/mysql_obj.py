#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crawl.db_connect import connectMysql

class MysqlObj(object):
    """docstring for MysqlObj"""
    def __init__(self):
        try:
            self.con = connectMysql()
            print(self.con)
            if self.con != False:
                self.cur = self.con.cursor()
            else:
                print("数据库连接失败")
        except:
            print( "数据库连接失败")

    
    def close(self):
        """关闭数据库连接"""
        if  self.con != False :
            self.con.close()
        else:
            raise "数据库关闭失败."    


    def executeSql(self,sql=''):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except Exception as e:
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print (error)

    def executeCommit(self,sql=''):
        """执行数据库sql语句，针对更新,删除,事务等操作失败时回滚

        """
        try:
            self.cur.execute(sql)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print ("error:", error)
            return False

    def insert(self, tablename, params):
        """创建数据库表

            args：
                tablename  ：表名字
                key        ：属性键
                value      ：属性值
        """
        key = []
        value = []
        for tmpkey, tmpvalue in params.items():
            key.append("`" + tmpkey + "`")
            if isinstance(tmpvalue, str):
                value.append("'" + tmpvalue + "'")
            else:
                value.append(tmpvalue)

        print (value)        
        attrs_sql = '('+','.join(key)+')'
        values_sql = ' values('+','.join(value)+')'

        sql = 'insert into %s'%tablename
        sql = sql + attrs_sql + values_sql
        print ('_insert:'+sql)
        self.executeCommit(sql)

    def select(self, tablename, cond_dict='', order='', fields='*',limit=10):
        """查询数据

            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件

            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                consql = consql+k  + v + ' and '
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename  
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename) 
            else:
                raise "fields input error, please input list fields."
        sql = sql + consql + order + 'limit %s ' % limit
        print ('select:' + sql)
        return self.executeSql(sql)

    def delete(self, tablename, cond_dict):
        """删除数据

            args：
                tablename  ：表名字
                cond_dict  ：删除条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)

        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        print (sql)
        return self.executeCommit(sql)


    def update(self, tablename, attrs_dict, cond_dict):
        """更新数据

            args：
                tablename  ：表名字
                attrs_dict  ：更新属性键值对字典
                cond_dict  ：更新条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)

        """
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" +"\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)

        print ("attrs_sql:", attrs_sql)
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename +"`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        print (sql)
        return self.executeCommit(sql)    
        