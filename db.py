# -*- coding:utf-8 -*-
# vim: set fileencoding=utf-8

import MySQLdb

class MysqlConnect(object):
    # 魔术方法, 初始化, 构造函数
    def __init__(self, host, user, passwd, db):
        '''
        :param host: IP
        :param user: 用户名
        :param password: 密码
        :param port: 端口号
        :param database: 数据库名
        :param charset: 编码格式
        '''
        self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, port=3306, db=db, charset='utf8')
        self.cursor = self.db.cursor()

    # 将要插入的数据写成元组传入
    def exec_data(self, sql, data=None):
        # 执行SQL语句
        self.cursor.execute(sql, data)
        # 提交到数据库执行
        self.db.commit()

    # sql拼接时使用repr()，将字符串原样输出
    def exec_sql(self, sql):
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()