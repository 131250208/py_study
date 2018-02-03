# -*- coding:utf-8 -*-
import pymysql
class DBManager:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "Database6981228.", "weibo")
        self.db.set_charset("utf8")
        cursor = self.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

    def insert_account(self, cookies_js, phone_num, password, quantity_level, uid):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO accounts(cookies_js, \
                         phone_num, quantity_level, uid, password) \
                         VALUES ('%s', '%s', '%d', '%s', '%s')" % \
              (pymysql.escape_string(cookies_js), pymysql.escape_string(phone_num),
               quantity_level, pymysql.escape_string(uid), pymysql.escape_string(password))
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
            print("insert_account error! row: ")
            print(phone_num)

    def count(self, username):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 查询语句
        sql = "SELECT count(*) FROM accounts WHERE phone_num = '%s'" % (username)

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return  results[0][0]
        except:
            print("Error: unable to fetch data")
            print("username")

    def get_accounts(self, level):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 查询语句
        sql = "SELECT cookies_js, uid, phone_num, password FROM accounts WHERE quantity_level = %d" % (level)

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Error: unable to fetch accounts, info: ")
            print(e)

    def get_cookies_uid(self, phone_num):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 查询语句
        sql = "SELECT cookies_js, uid FROM accounts WHERE phone_num = '%s'" % (phone_num)

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Error: unable to fetch data, info: ")
            print(e)

    def update_password(self, username, password):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 插入语句
        sql = "UPDATE accounts SET password = '%s' WHERE phone_num = '%s'" % (password, username)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            print("update_password error! username: %s" % (username))
            print(e)

    def update_cookies(self, cookies_js, username):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # SQL 插入语句
        sql = "UPDATE accounts SET cookies_js = '%s' WHERE phone_num = '%s'" % (cookies_js, username)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            print("update_password error! username: %s" % (username))
            print(e)

    def db_close(self):
        # 关闭数据库连接
        self.db.close()

if __name__ == "__main__":
    pass