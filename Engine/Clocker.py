
from BaseObserver import Observer
from SpiderServer import SpiderServer

# 更新账户信息指令
from settings import REFRESH_ALL
from settings import REFRESH_VIDEO_CONTENT
from settings import REFRESH_HOMEPAGE
from settings import REFRESH_LOGOSRC
from settings import REFRESH_ADS
from settings import REFRESH_INFO


#url保存在redis数据库中的键名
from settings import FB_HOMEPAGE_URL
#url保存在redis数据库中的键名
from settings import FB_VIDEO_ADS_URL
#url保存在redis数据库中的键名
from settings import FB_VIDEO_CONTENT_URL
#url保存在redis数据库中的键名
from settings import FB_VIDEO_INFO_URL


class Clocker(Observer):
    '''
    定时任务，按天更新redis
    '''
    def __init__(self,server_redis,logger):
        #创建连接本地server端redis
        self.server_redis = server_redis
        self.logger = logger


    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == REFRESH_ALL:
            self.logger.info("启动定时任务，开始更新redis...")
            self.deleteRedisKey()
            self.server_redis.delete(REFRESH_ALL)

    def deleteRedisKey(self):
        rediskeys = [
                      FB_VIDEO_ADS_URL + '_set',
                      FB_VIDEO_CONTENT_URL + '_set',
                      FB_VIDEO_INFO_URL + '_set',
                    ]
        for key in rediskeys:
            # 清除历史账户登录信息和cookies信息
            self.logger.info("定时任务: 删除 %s"%key)
            self.server_redis.delete(key)
        #给主控制节点发送数据更新请求
        request_list = [
                    REFRESH_ADS,
                    REFRESH_HOMEPAGE,
                    REFRESH_INFO,
                    REFRESH_LOGOSRC,
                    REFRESH_VIDEO_CONTENT
                  ]
        for key in request_list:
            # 更新cookies
            self.server_redis.lpush(key, key)
            self.logger.info("send_request: %s"%key)