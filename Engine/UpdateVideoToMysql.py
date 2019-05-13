from BaseObserver import Observer
from SpiderServer import SpiderServer

import os
import sys

try:
    import cpickle as pickle
except:
    import pickle

# 视频预览图、视频、音频、logo保存路径
from settings import IMAGES_STORE
from settings import VIDEO_STORE
from settings import VIDEOIMG_STORE
from settings import AUDIO_STORE

# SaveVideoSpider爬取到的数据保存在redis
from settings import VIDEO_CONTENT_DATA


class UpdateVideoToMysql(Observer):
    '''
    该模式用于保存数据
    功能：更新视频的首帧图、视频、音频的服务器保存路径
    '''

    def __init__(self, server_redis, client_redis, logger, dbhelper):
        super().__init__()
        # 创建连接server_redis本地端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper

        # 获取当前文件所在绝对路径
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.abspath = '/'.join(self.abspath.split('/')[:-1])
        self.download_file()

    def download_file(self):
        # 将下载的视频、图片、音频保存在本地
        paths = [IMAGES_STORE, VIDEO_STORE, VIDEOIMG_STORE, AUDIO_STORE]
        for path in paths:
            directory = os.path.join(self.abspath, path)
            if not os.path.exists(directory):
                os.makedirs(directory)

    def updateVideo(self, datas):
        store_imgSrc = []
        store_videoUrl = []
        store_radioUrl = []
        store_logoSrc = []
        path_list = []
        for data in datas:
            item = pickle.loads(data)
            path_file = ''
            if item.get('imgSrc', None):
                store_imgSrc.append((item['imgSrc'], item['videoId']))
                path_file = (item['imgSrc'], item['file_content'])
            elif item.get('videoUrl', None):
                store_videoUrl.append((item['videoUrl'], item['isDownload'], \
                                       item['lastUpdateDate'], item['videoId']))
                path_file = (item['videoUrl'], item['file_content'])
            elif item.get('radioUrl', None):
                store_radioUrl.append((item['radioUrl'], item['videoId']))
                path_file = (item['radioUrl'], item['file_content'])
            elif item.get('logoSrc', None):
                store_logoSrc.append((item['logoSrc'], item['isDownload'], item['pageId']))
                path_file = (item['logoSrc'], item['file_content'])
            # 保存文件
            if path_file:
                self.download(*path_file)
        if store_imgSrc:
            values = ', '.join(['%s'] * len(store_imgSrc))
            sql = 'insert into fb_video (imgSrc,videoId) values %s \
                   on duplicate key update imgSrc=values(imgSrc)' % values
            self.dbhelper.insert(sql % tuple(store_imgSrc))
        if store_videoUrl:
            values = ', '.join(['%s'] * len(store_videoUrl))
            sql = 'insert into fb_video (videoUrl,isDownload,lastUpdateDate,videoId) values %s \
                   on duplicate key update videoUrl=values(videoUrl),isDownload=values(isDownload),lastUpdateDate=values(lastUpdateDate)' % values
            self.dbhelper.insert(sql % tuple(store_videoUrl))
        if store_radioUrl:
            values = ', '.join(['%s'] * len(store_radioUrl))
            sql = 'insert into fb_video (radioUrl,videoId) values %s \
                   on duplicate key update radioUrl=values(radioUrl)' % values
            self.dbhelper.insert(sql % tuple(store_radioUrl))
        if store_logoSrc:
            values = ', '.join(['%s'] * len(store_logoSrc))
            sql = 'insert into fb_homepage (logoSrc,isDownload,pageId) values %s on duplicate key update logoSrc=values(logoSrc),isDownload=values(isDownload);' % values
            self.dbhelper.insert(sql % tuple(store_logoSrc))
            print(sql % tuple(store_logoSrc))

        # #将数据保存在本地服务器
        # for path in path_list:
        #     self.download(*path)

    def download(self, path, data):
        if not data:
            return
        directory = os.path.join(self.abspath, path)
        # 判断文件是否存在
        flag = os.path.exists(directory)
        if flag:
            self.logger.info(path + " 已存在！")
            return

        with open(directory, 'wb') as file:
            file.write(data)
            file.flush()

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == VIDEO_CONTENT_DATA:
            # 判断客户端是否有VIDEO_DATA
            if self.server_redis.exists(VIDEO_CONTENT_DATA):
                datas = []
                num = 0
                while num < 100:
                    data = self.server_redis.rpop(VIDEO_CONTENT_DATA)
                    if not data:
                        break
                    datas.append(data)
                    num += 1
            else:
                return
            self.updateVideo(datas)
            self.logger.info("保存 %s 完毕！" % VIDEO_CONTENT_DATA)
