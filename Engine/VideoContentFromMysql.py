
import hashlib
import json

from BaseObserver import Observer
from SpiderServer import SpiderServer


#url保存在redis数据库中的键名
from settings import FB_VIDEO_CONTENT_URL
# 更新账户信息指令
from settings import REFRESH_VIDEO_CONTENT





class VideoContentFromMysql(Observer):
    '''
    该模式用于从Mysql数据库取数据
    功能：从数据库中获取视频广告的首帧图、视频、音频的下载链接
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper
        self.__videoContent = []



    def setVideoContent(self):
        sql = "select videoId, videoImg, originVideoUrl, originRadio from fb_video where isDownload=0"
        datas = self.dbhelper.select(sql)
        if not datas:
            return
        for data in datas:
            videoId, videoImg, originVideoUrl, originRadio = tuple(data)
            if originVideoUrl:
                self.__videoContent.append({'videoId':videoId, 'originVideoUrl':originVideoUrl})
                if videoImg:
                    self.__videoContent.append({'videoId':videoId, 'videoImg':videoImg})
                if originRadio:
                    self.__videoContent.append({'videoId':videoId, 'originRadio': originRadio})

    def refreshVideoContent(self):
        # 将数据放入到redis中
        for video in self.__videoContent:
            data_json = json.dumps(video, ensure_ascii=False)
            finger = self.fingerPrint(data_json)
            flag = self.server_redis.sismember(FB_VIDEO_CONTENT_URL + "_set", finger)
            if not flag:
                self.server_redis.sadd(FB_VIDEO_CONTENT_URL, data_json)
                self.server_redis.sadd(FB_VIDEO_CONTENT_URL + "_set", finger)
        self.__videoContent = []




    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode("utf-8")).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger


    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_VIDEO_CONTENT:
            self.setVideoContent()
            self.refreshVideoContent()
            self.server_redis.delete(REFRESH_VIDEO_CONTENT)
            self.logger.info("%s 完毕！"%REFRESH_VIDEO_CONTENT)