

from BaseObserver import Observer
from SpiderServer import SpiderServer


import json


#VideoSpider爬取到的数据保存在redis
from settings import VIDEO_DATA


class VideoToMysql(Observer):
    '''
    该模式用于保存数据
    功能：将视频信息保存到数据库
    '''
    def __init__(self,server_redis,client_redis,logger,dbhelper):
        super().__init__()
        #创建连接server_redis本地端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper

    def storeVideo(self,datas):
        if not datas:
            return
        # 保存到fb_video表
        try:
            keys = ''
            values = []
            for data in datas:
                try:
                   data = json.loads(data.decode('utf-8'))
                except:
                    continue
                # 更新fb_homepage状态
                self.updateHomepage(data)
                if 'pageUrl' in data.keys():
                    continue
                elif not keys:
                    keys = ', '.join(data.keys())
                s = ["'" + str(i) + "'" for i in tuple(data.values())]
                item = "(" + ','.join(s) + ")"
                values.append(item)
            if values:
                values = ','.join(values)
                # 保存到fb_video表中
                sql = 'insert ignore into fb_video (%s) values %s '%(keys, values)
                self.dbhelper.insert(sql)
                self.logger.info("保存 %s 完毕！"%VIDEO_DATA)
        except Exception as e:
            self.logger.exception(e)




    def updateHomepage(self,data):
        if not data:
            return
        try:
            if 'pageId' in data.keys():
                sql = "update fb_homepage set status=IF(status>=30, 30, status+1) WHERE pageId='%s'"%data['pageId']
            elif 'pageUrl' in data.keys():
                sql = "update fb_homepage set status=IF(status<=0, 0, status-1) WHERE url='%s'"%data['pageUrl']
            else:
                return
            self.dbhelper.insert(sql)
        except Exception as e:
            self.logger.exception(e)



    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == VIDEO_DATA:
            if self.server_redis.exists(VIDEO_DATA):
                datas = []
                num = 0
                while num < 100:
                    data = self.server_redis.rpop(VIDEO_DATA)
                    if not data:
                        break
                    datas.append(data)
                    num += 1
            else:
                return
            self.storeVideo(datas)
            self.logger.info("保存 %s 完毕！"%VIDEO_DATA)

