
import time
import hashlib
import json

from BaseObserver import Observer
from SpiderServer import SpiderServer


#url保存在redis数据库中的键名
from settings import FB_HOMEPAGE_URL
# 更新账户信息指令
from settings import REFRESH_HOMEPAGE





class HomepageFromMysql(Observer):
    '''
    该模式用于从Mysql数据库取数据
    功能：从数据库中获取主页URL
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper
        self.__homepage = []


    def setHomepage(self):
        sql = "select url from fb_items where status>0 order by status DESC"
        datas = self.dbhelper.select(sql)
        if not datas:
            return
        for data in datas:
            url = tuple(data)
            if url:
                self.__homepage.append(url[0])

    def refreshHomepage(self):
        # 将数据放入到redis中
        if not self.server_redis.exists(FB_HOMEPAGE_URL):
            self.server_redis.delete(FB_HOMEPAGE_URL + '_set')
        for url in self.__homepage:
            finger = self.fingerPrint(url)
            flag = self.server_redis.sismember(FB_HOMEPAGE_URL + "_set", finger)
            if not flag:
                self.server_redis.lpush(FB_HOMEPAGE_URL, url)
                self.server_redis.sadd(FB_HOMEPAGE_URL + "_set", finger)
        self.__homepage = []


    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode("utf-8")).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger


    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_HOMEPAGE:
            self.setHomepage()
            self.refreshHomepage()
            self.server_redis.delete(REFRESH_HOMEPAGE)
            self.logger.info("%s 完毕！"%REFRESH_HOMEPAGE)