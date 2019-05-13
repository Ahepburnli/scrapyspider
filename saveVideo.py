


from startSpider.SaveVideoSpider import SaveVideoSpider

from startSpider.Person import Person
from startSpider.Request import Request



from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler
from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_SAVEVIDEO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT
from scrapyuniversal.settings import REFRESH_INFO
from scrapyuniversal.settings import REFRESH_VIDEO_CONTENT
from scrapyuniversal.settings import REFRESH_LOGOSRC
from scrapyuniversal.settings import FB_VIDEO_CONTENT_URL

import time
import datetime
import schedule

class Spider():
    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_SAVEVIDEO)
        self.loggers = self.loggershelper.Loggers()
        self.saveVideoSpider = SaveVideoSpider("saveVideoSpider", "下载视频、音频和图片",self.loggers,self.client_redis)
        # 设置定时任务
        self.__date = time.strftime("%Y-%m-%d",time.localtime())
        self.__saveVideo = Person()
        self.__saveVideo.setLeader(self.saveVideoSpider)



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


    def saveVideo(self):
        # 更新视频链接
        self.client_redis.lpush(REFRESH_LOGOSRC, REFRESH_LOGOSRC)
        self.client_redis.lpush(REFRESH_VIDEO_CONTENT, REFRESH_VIDEO_CONTENT)
        time.sleep(20)
        if self.client_redis.exists(FB_VIDEO_CONTENT_URL):
            self.__saveVideo.sendReuqest(Request('saveVideo'))


    def main(self):
        # 每20分钟执行一次
        schedule.every(20).minutes.do(self.saveVideo)

        while True:
            self.setDate()
            schedule.run_pending()
            time.sleep(1)




if __name__ == "__main__":
    spider = Spider()
    spider.main()
    #spider.saveVideo()
