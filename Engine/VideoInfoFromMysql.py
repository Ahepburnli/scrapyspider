
import json
import hashlib

from BaseObserver import Observer
from SpiderServer import SpiderServer


#url保存在redis数据库中的键名
from settings import FB_VIDEO_INFO_URL
#启动VideoInfoSpider需要的url
from settings import PAGEVIEWURL

# 更新账户信息指令
from settings import REFRESH_INFO




class VideoInfoFromMysql(Observer):
    '''
    该模式用于从Mysql数据库取数据
    功能：从数据库中获取视频的预览链接
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper
        self.__info = []

    def setInfo(self):
        sql = "select pageviewUrl from fb_video where status>0 order by status DESC"
        datas = self.dbhelper.select(sql)
        if not datas:
            return
        for data in datas:
            url = tuple(data)
            if url:
                self.__info.append(url[0])

    def refreshInfo(self):
        # 将数据放入到redis中
        for url in self.__info:
            finger = self.fingerPrint(url)
            flag = self.server_redis.sismember(FB_VIDEO_INFO_URL + "_set", finger)
            if not flag:
                self.server_redis.sadd(FB_VIDEO_INFO_URL, url)
                self.server_redis.sadd(FB_VIDEO_INFO_URL+ "_set", finger)
        self.__info = []


    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode("utf-8")).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_INFO:
            self.setInfo()
            self.refreshInfo()
            self.server_redis.delete(REFRESH_INFO)
            self.logger.info("%s 完毕！"%REFRESH_INFO)

