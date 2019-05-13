import pymysql
import time

#MYSQL连接设置
from settings import MYSQL_HOST
from settings import MYSQL_PORT
from settings import MYSQL_USER
from settings import MYSQL_PWD
from settings import MYSQL_DB
from settings import MYSQL_CHARSET

class DBHelper:
    """
    完成所有对mysql数据库的处理
    """
    def __init__(self, logger=None):
        self.host = MYSQL_HOST
        self.user = MYSQL_USER
        self.pwd = MYSQL_PWD
        self.db = MYSQL_DB
        self.port = MYSQL_PORT
        self.charset = MYSQL_CHARSET
        self.conn = None#连接
        self.cur = None#游标
        self.logger = logger

    def connectDataBase(self):
        """
         连接数据库
        """
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user,
                                        password=self.pwd, port=self.port,
                                        database=self.db, charset=self.charset
                                        )
        except:
            return False
        self.cur = self.conn.cursor()
        return True

    def close(self):
        """
        关闭数据库
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        return True

    def select(self, sql, params=None):
        """
        执行SQL
        """
        while True:
            if self.connectDataBase():
                break
            else:
                time.sleep(1)
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
                data = self.cur.fetchall()
                return data
        except Exception as e:
            self.logger.exception(e)
            return None

    def insert(self, sql, params=None):
        """
        执行SQL
        """
        while True:
            if self.connectDataBase():
                break
            else:
                time.sleep(1)
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            print(sql,params)
            self.logger.exception(e)
            return False
        return True

    def insert_many(self, sql, params=None):
        """
        执行SQL
        """
        while True:
            if self.connectDataBase():
                break
            else:
                time.sleep(1)
        try:
            if self.conn and self.cur:
                self.cur.executemany(sql, params)
                self.conn.commit()
        except Exception as e:
            print(sql,params)
            self.logger.exception(e)
            return False
        return True




if __name__ == '__main__':
    dbhelper = DBHelper()
    print(dbhelper.connectDataBase())

