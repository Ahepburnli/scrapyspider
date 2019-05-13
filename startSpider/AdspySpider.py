from startSpider.Responsible import Responsible

import os

class AdspySpider(Responsible):
    """主管"""

    def __init__(self, name, title,loggers):
        super().__init__(name, title)
        self.loggers = loggers


    def _handleRequestImpl(self, request):
        if (request.getReason() == 'homepage'):
            self.loggers.info("启动：%s(%s)" % (self.getName(), self.getTitle()))
            os.system("scrapy crawl adspySpider")




