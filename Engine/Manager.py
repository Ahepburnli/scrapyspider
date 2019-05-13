import time
import os
import sys
import datetime
import gevent
from gevent import monkey

monkey.patch_all()  # 识别等待时间，让协程切换

from SpiderServer import SpiderServer
from AdsFromMysql import AdsFromMysql
from Clocker import Clocker
from HomepageToMysql import HomepageToMysql
from HomepageFromMysql import HomepageFromMysql
from LogoSrcFromMysql import LogoSrcFromMysql
from UpdateVideoToMysql import UpdateVideoToMysql
from VideoContentFromMysql import VideoContentFromMysql
from VideoInfoFromMysql import VideoInfoFromMysql
from VideoToMysql import VideoToMysql
from VideoInfoToMysql import VideoInfoToMysql

try:
    from RedisHelper.RedisHelper import RedisHandler
except:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    from RedisHelper.RedisHelper import RedisHandler

from MySqlHelper import DBHelper
from LoggerHelper.LogHelper import LoggersHelper
from settings import LOG_LEVEL
from settings import FILENAME
from settings import CLIENT_HOST
from settings import CLIENT_DB
from settings import CLIENT_PASSWORD
from settings import CLIENT_PORT
from settings import SERVER_HOST
from settings import SERVER_PORT
from settings import SERVER_DB
from settings import SERVER_PASSWORD

# 信息指令,用于请求数据
# 请求账户
from settings import REFRESH_ACCOUNTS
# 请求所有
from settings import REFRESH_ALL
# 请求视频、音频、图片下载链接
from settings import REFRESH_VIDEO_CONTENT
# 请求主页链接
from settings import REFRESH_HOMEPAGE
# 请求主页logo下载链接
from settings import REFRESH_LOGOSRC
# 请求主页链接，用于获取信息与广告，供爬虫子节点使用
from settings import REFRESH_ADS
# 请求视频预览链接
from settings import REFRESH_INFO
# HomepageSpider爬取到的数据保存在redis
from settings import HOMEPAGE_DATA
# VideoSpider爬取到的数据保存在redis
from settings import VIDEO_DATA
# SaveVideoSpider爬取到的数据保存在redis
from settings import VIDEO_CONTENT_DATA
# VideoInfoSpider爬取到的数据保存在redis
from settings import VIDEO_INFO_DATA

LISTEN = [
    REFRESH_ACCOUNTS, REFRESH_VIDEO_CONTENT, REFRESH_HOMEPAGE,
    REFRESH_LOGOSRC, REFRESH_ADS, REFRESH_INFO, REFRESH_ALL,
    HOMEPAGE_DATA, VIDEO_DATA, VIDEO_CONTENT_DATA, VIDEO_INFO_DATA
]


class Manager():
    def __init__(self):
        # 创建连接远程客户端redis
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建连接本地server端redis
        self.server_redis = RedisHandler(SERVER_HOST, SERVER_PORT, SERVER_DB, SERVER_PASSWORD)
        self.server_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, FILENAME)
        self.logger = self.loggershelper.Loggers()
        # 创建Mysql数据库连接
        self.dbhelper = DBHelper(self.logger)
        # 创建监听实例
        self.server = SpiderServer(self.logger)
        self.clocker = Clocker(self.server_redis, self.logger)
        params = (self.server_redis, self.client_redis, self.logger, self.dbhelper)
        # self.account_from_mysql = AccountFromMysql(*params)
        self.ads_from_mysql = AdsFromMysql(*params)
        # self.cookie_from_mysql = CookieFromMysql(*params)
        # self.cookie_to_mysql = CookieToMysql(*params)
        self.homepage_to_mysql = HomepageToMysql(*params)
        self.homepage_from_mysql = HomepageFromMysql(*params)
        self.logoSrc_from_mysql = LogoSrcFromMysql(*params)
        # self.testCookie_from_mysql = TestCookieToMysql(*params)
        self.updateVideo_to_mysql = UpdateVideoToMysql(*params)
        self.videoContent_from_mysql = VideoContentFromMysql(*params)
        self.videoInfo_from_mysql = VideoInfoFromMysql(*params)
        self.video_to_mysql = VideoToMysql(*params)
        self.videoInfo_to_mysql = VideoInfoToMysql(*params)
        # self.videoAds_from_server_to_client = VideoAdsFromServerToClient(*params)
        self.server.addObserver(self.clocker)
        # self.server.addObserver(self.account_from_mysql)
        self.server.addObserver(self.ads_from_mysql)
        # self.server.addObserver(self.cookie_to_mysql)
        # self.server.addObserver(self.cookie_from_mysql)
        self.server.addObserver(self.homepage_to_mysql)
        self.server.addObserver(self.homepage_from_mysql)
        self.server.addObserver(self.logoSrc_from_mysql)
        # self.server.addObserver(self.testCookie_from_mysql)
        self.server.addObserver(self.updateVideo_to_mysql)
        self.server.addObserver(self.videoContent_from_mysql)
        self.server.addObserver(self.videoInfo_from_mysql)
        self.server.addObserver(self.video_to_mysql)
        self.server.addObserver(self.videoInfo_to_mysql)
        # self.server.addObserver(self.videoAds_from_server_to_client)

        # 设置定时任务
        self.__date = time.strftime("%Y-%m-%d", time.localtime())
        self.logger.info("进程 %d：Manager 准备完毕..." % os.getpid())
        self.__listen = LISTEN

    def setDate(self):
        # 更改日志保存目录
        localtime = time.strftime("%Y-%m-%d", time.localtime())
        day1 = datetime.datetime.strptime(localtime, '%Y-%m-%d')
        day2 = datetime.datetime.strptime(self.__date, '%Y-%m-%d')
        delday = day1 - day2
        if delday.days == 1:
            self.logger.removeHandler(self.loggershelper.file_handler)
            self.logger = self.loggershelper.NewLoggers()
            self.server.setMessage(REFRESH_ALL)
            self.__date = localtime
            self.logger.info("更新日志目录，进程 %d：Manager 正在运行..." % os.getpid())

    def main(self):
        print("开始监听...")
        while True:
            try:
                # 监控本地server端
                for key in self.__listen:
                    if self.server_redis.exists(key):
                        # 创建协程实现多任务
                        g1 = gevent.spawn(self.server.setMessage, key)
                        g1.join()
                self.setDate()
            except KeyboardInterrupt:
                os._exit(0)
            except Exception as e:
                self.logger.exception(e)


if __name__ == "__main__":
    manager = Manager()
    manager.main()
