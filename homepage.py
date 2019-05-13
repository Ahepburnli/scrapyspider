from startSpider.AdSectorSpider import AdSectorSpider
from startSpider.GetVideoSpider import GetVideoSpider
from startSpider.AdspySpider import AdspySpider
from startSpider.HomepageSpider import HomepageSpider
from startSpider.SaveVideoSpider import SaveVideoSpider
from startSpider.VideoInfoSpider import VideoInfoSpider
from startSpider.Person import Person
from startSpider.Request import Request

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler
from scrapyuniversal.settings import LOG_LEVEL  # 日志等级
from scrapyuniversal.settings import NAME_HOMEPAGE
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
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_HOMEPAGE)
        self.loggers = self.loggershelper.Loggers()
        self.directLeader = AdspySpider('adspySpider','爬取adspySpider.com网站',self.loggers)
        self.adSectorSpider = AdSectorSpider('adSectorSpider','爬取adSector.com网站',self.loggers)
        self.getVideoSpider = GetVideoSpider("getVideoSpider", "爬取adSector.com网站的视频详情", self.client_redis, self.loggers)
        self.homepageSpider = HomepageSpider("homepageSpider", "爬取facebook主页信息", self.client_redis, self.loggers)
        self.directLeader.setNextHandler(self.adSectorSpider)
        self.adSectorSpider.setNextHandler(self.homepageSpider)
        self.homepageSpider.setNextHandler(self.getVideoSpider)

        # 设置定时任务
        self.__date = time.strftime("%Y-%m-%d", time.localtime())
        self.__homepage = Person()
        # self.__homepage.setLeader(self.directLeader)

    def setDate(self):
        # 更改日志保存目录
        localtime = time.strftime("%Y-%m-%d", time.localtime())
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

    def gethomepage(self):
        # 爬取主页信息
        self.__homepage.sendReuqest(Request('homepage'))

    def main(self):
        # 每6小时执行
        schedule.every(6).hours.do(self.gethomepage)

        while True:
            self.setDate()
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    spider = Spider()
    spider.main()
    # spider.gethomepage()
