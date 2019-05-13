from startSpider.Responsible import Responsible



from scrapyuniversal.settings import ADS_VIDEO

import os
import time



class GetVideoSpider(Responsible):
    """CEO"""

    def __init__(self, name, title, client_redis,loggers):
        super().__init__(name, title)
        self.client_redis = client_redis
        self.loggers = loggers


    def _handleRequestImpl(self, request):
        if (request.getReason() == "homepage" or request.getReason() == 'video')\
                and self.client_redis.exists(ADS_VIDEO):
            self.loggers.info("启动：%s(%s)" % (self.getName(), self.getTitle()))
            os.system("scrapy crawl getVideoSpider")



