

from BaseObserver import Observer
from SpiderServer import SpiderServer

import json
import copy

#VideoInfoSpider爬取到的数据保存在redis
from settings import VIDEO_INFO_DATA


class VideoInfoToMysql(Observer):
    '''
    该模式用于保存数据
    功能：保存视频的浏览、点赞、评论等信息量
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接server_redis本地端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper

    def storeVideoInfo(self,datas):
        try:
            key_s = []
            keys = ''
            values = []
            for data in datas:
                try:
                   data = json.loads(data.decode('utf-8'))
                except:
                    continue
                if not keys:
                    keys = ', '.join(data.keys())
                    for key,value in data.items():
                        key_s.append(key + '=values(' + key + ')')
                    key_s = ','.join(key_s)
                s = [str(i) for i in tuple(data.values())]
                item = "(" + ','.join(s) + ")"
                values.append(item)
            values = ','.join(values)
            # 保存到fb_video表中
            sql = 'insert into fb_video (%s) values %s on duplicate key update %s'%(keys, values, key_s)
            self.dbhelper.insert(sql)
            # 保存到video_info列表中(记录每次爬取记录)
            sql = 'insert ignore into fb_video_list (%s) values %s' % (keys, values)
            self.dbhelper.insert(sql)
            self.logger.info("保存 %s 完毕！"%VIDEO_INFO_DATA)
        except Exception as e:
            self.logger.exception(e)

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == VIDEO_INFO_DATA:
            datas = []
            num = 0
            while num < 100:
                data = self.server_redis.rpop(VIDEO_INFO_DATA)
                if not data:
                    break
                datas.append(data)
                num += 1
            if datas:
                self.storeVideoInfo(datas)