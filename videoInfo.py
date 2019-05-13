


from startSpider.VideoInfoSpider import VideoInfoSpider
from startSpider.Person import Person
from startSpider.Request import Request

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler
from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_VIDEO_INFO

from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT
from scrapyuniversal.settings import REFRESH_INFO
from scrapyuniversal.settings import REFRESH_VIDEO_CONTENT
from scrapyuniversal.settings import REFRESH_LOGOSRC

import time
import datetime
import schedule



class Spider():
    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_VIDEO_INFO)
        self.loggers = self.loggershelper.Loggers()
        self.videoInfoSpider = VideoInfoSpider("videoInfoSpider", "爬取视频评论、观看、点赞等信息",self.loggers,self.client_redis)

        # 设置定时任务
        self.__date = time.strftime("%Y-%m-%d",time.localtime())
        self.__videoInfo = Person()
        self.__videoInfo.setLeader(self.videoInfoSpider)




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


    def videoInfo(self):
        self.client_redis.lpush(REFRESH_INFO, REFRESH_INFO)
        time.sleep(20)
        self.__videoInfo.sendReuqest(Request('videoInfo'))

    def main(self):
        # 每天00:30执行
        schedule.every().day.at("12:25").do(self.videoInfo)

        while True:
            self.setDate()
            schedule.run_pending()
            time.sleep(1)




if __name__ == "__main__":
    spider = Spider()
    spider.main()
    #spider.videoInfo()
