

import hashlib
import json

from BaseObserver import Observer
from SpiderServer import SpiderServer


#url保存在redis数据库中的键名
from settings import FB_VIDEO_CONTENT_URL

# 更新账户信息指令
from settings import REFRESH_LOGOSRC



class LogoSrcFromMysql(Observer):
    '''
    该模式用于从Mysql数据库取数据
    功能：从数据库中获取主页logo图链接
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper
        self.__logoSRC = []



    def setLogoSRC(self):
        sql = "select pageId, originalLogoSrc from fb_homepage where isDownload=0"
        datas = self.dbhelper.select(sql)
        if not datas:
            return
        for data in datas:
            pageId, originalLogoSrc = tuple(data)
            if originalLogoSrc:
                self.__logoSRC.append({'pageId':pageId,'originalLogoSrc':originalLogoSrc})

    def refreshLogoSRC(self):
        # 将数据放入到redis中
        for logo in self.__logoSRC:
            data_json = json.dumps(logo, ensure_ascii=False)
            finger = self.fingerPrint(data_json)
            flag = self.server_redis.sismember(FB_VIDEO_CONTENT_URL  + "_set", finger)
            if not flag:
                self.server_redis.sadd(FB_VIDEO_CONTENT_URL , data_json)
                self.server_redis.sadd(FB_VIDEO_CONTENT_URL + "_set", finger)
        self.__logoSRC = []

    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode("utf-8")).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_LOGOSRC:
            self.setLogoSRC()
            self.refreshLogoSRC()
            self.server_redis.delete(REFRESH_LOGOSRC)
            self.logger.info("%s 完毕！"%REFRESH_LOGOSRC)
