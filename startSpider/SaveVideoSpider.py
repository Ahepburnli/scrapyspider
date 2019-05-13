from startSpider.Responsible import Responsible

from scrapyuniversal.settings import FB_VIDEO_CONTENT_URL

import os


class SaveVideoSpider(Responsible):
    """部门总监"""

    def __init__(self, name, title,loggers, client_redis):
        super().__init__(name, title)
        self.loggers = loggers
        self.client_redis = client_redis

    def _handleRequestImpl(self, request):
        if (request.getReason() == 'saveVideo') \
                and self.client_redis.exists(FB_VIDEO_CONTENT_URL):
            self.loggers.info("启动：%s(%s)" % (self.getName(), self.getTitle()))
            os.system("scrapy crawl saveVideoSpider")



