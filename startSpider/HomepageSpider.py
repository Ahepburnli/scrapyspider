from startSpider.Responsible import Responsible
from scrapyuniversal.settings import REFRESH_HOMEPAGE

import os
import time


class HomepageSpider(Responsible):
    """行政人员"""

    def __init__(self, name, title, client_redis, loggers):
        super().__init__(name, title)
        self.client_redis = client_redis
        self.loggers = loggers

    def _handleRequestImpl(self, request):
        if request.getReason() == "homepage" :
            self.loggers.info("启动：%s(%s)" % (self.getName(), self.getTitle()))
            self.client_redis.lpush(REFRESH_HOMEPAGE,REFRESH_HOMEPAGE)
            time.sleep(20)
            os.system("scrapy crawl homepageSpider")



