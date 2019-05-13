
from startSpider.GetVideoSpider import GetVideoSpider
from startSpider.VideoSpider import VideoSpider


from startSpider.Person import Person
from startSpider.Request import Request

import os
import time
import datetime
import schedule


from scrapyuniversal.settings import FB_VIDEO_ADS_URL
from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_VIDEO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT
from scrapyuniversal.settings import REFRESH_ADS

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler




class Spider():
    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_VIDEO)
        self.loggers = self.loggershelper.Loggers()
        self.videoSpider = VideoSpider('videoSpider','爬取facebook信息与广告',self.loggers,self.client_redis)
        self.getVideoSpider = GetVideoSpider("getVideoSpider", "爬取facebook的视频详情",self.client_redis,self.loggers)
        self.videoSpider.setNextHandler(self.getVideoSpider)
        # 设置定时任务
        self.__date = time.strftime("%Y-%m-%d",time.localtime())
        self.__video = Person()
        self.__video.setLeader(self.videoSpider)




    def setDate(self):
        # 更改日志保存目录
        localtime = time.strftime("%Y-%m-%d",time.localtime())
        day1 = datetime.datetime.strptime(localtime, '%Y-%m-%d')
        day2 = datetime.datetime.strptime(self.__date, '%Y-%m-%d')
        delday = day1 - day2
        if delday.days == 1:
            self.loggers.removeHandler(self.loggershelper.file_handler)
            self.loggers = self.loggershelper.NewLoggers()
            self.__date = localtime
            return True
        else:
            return False

    def getVideo(self):
        try:
            self.client_redis.delete(FB_VIDEO_ADS_URL + '_set')
            self.client_redis.lpush(REFRESH_ADS, REFRESH_ADS)
            time.sleep(20)
            if self.client_redis.exists(FB_VIDEO_ADS_URL):
                # 爬取主页信息
                self.__video.sendReuqest(Request('video'))
        except Exception as e:
            self.loggers.exception(e)



    def main(self):
        # 每6小时执行
        schedule.every(6).hours.do(self.getVideo)


        while True:
            self.setDate()
            schedule.run_pending()
            time.sleep(1)





if __name__ == "__main__":
    spider = Spider()
    spider.main()
    #spider.getVideo()
