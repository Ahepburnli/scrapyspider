

import hashlib
import json

from BaseObserver import Observer
from SpiderServer import SpiderServer


#启动VideoSpider需要的主页url
from settings import VIDEO_ADS_URL
#url保存在redis数据库中的键名
from settings import FB_VIDEO_ADS_URL

# 更新账户信息指令
from settings import REFRESH_ADS







class AdsFromMysql(Observer):
    '''
    该模式用于从Mysql数据库取数据
    功能：从数据库中获取视频广告的主页URL
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper
        self.__ADS = []


    def setADS(self):
        sql = "select pageId,url from fb_homepage where status>0 order by status DESC"
        datas = self.dbhelper.select(sql)
        if not datas:
            return
        for data in datas:
            pageId, url = tuple(data)
            if pageId and url:
                self.__ADS.append({'pageId': pageId, 'url': url})

    def refreshADS(self):
        # 将数据放入到redis中
        if not self.__ADS:
            return
        for ads in self.__ADS:
            data_json = json.dumps(ads, ensure_ascii=False)
            finger = self.fingerPrint(ads['pageId'])
            flag = self.client_redis.sismember(FB_VIDEO_ADS_URL + "_set", finger)
            if not flag:
                self.client_redis.lpush(FB_VIDEO_ADS_URL, data_json)
                self.client_redis.sadd(FB_VIDEO_ADS_URL + "_set", finger)
        self.__ADS = []

    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode("utf-8")).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_ADS:
            self.setADS()
            self.refreshADS()
            self.server_redis.delete(REFRESH_ADS)
            self.logger.info("%s 完毕！"%REFRESH_ADS)
