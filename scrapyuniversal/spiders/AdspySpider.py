# -*- coding: utf-8 -*-
import scrapy
import time
import re
import os
import datetime
import random
from scrapyuniversal.items.Fb_Video_Item import fb_video_Item
from lxml import etree

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler

from scrapyuniversal.settings import LOG_LEVEL  # 日志等级
from scrapyuniversal.settings import NAME_ADSPYSPIDER
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.xlib.pydispatch import dispatcher  # 信号分发器
from scrapy import signals  # 信号


class AdspySpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = 'adspySpider'
    allowed_domains = ['api.adspy.com']
    start_urls = ['https://app.adspy.com/login']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapyuniversal.middlewares.AdspyChromeMiddleware.AdspyChromeMiddleware': 120,
        },
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.AdspyRedisPipeline.AdspyRedisPipeline': 34,
        },
        # 抓捕500异常
        'HTTPERROR_ALLOWED_CODES': [500],
        # 是否启动重试
        'RETRY_ENABLED': False,
        'DOWNLOAD_DELAY': random.random() * 2,
        # The initial download delay
        'AUTOTHROTTLE_START_DELAY': 0.01,
        # The maximum download delay to be set in case of high latencies
        'AUTOTHROTTLE_MAX_DELAY': 0.1,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_IP': 32,
    }

    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_ADSPYSPIDER)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("AdspySpider启动...")
        # chrome无头版
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # self.browser = webdriver.Chrome()
        # #浏览器窗口大小
        # self.browser.set_window_size(1400, 700)
        super(AdspySpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # 信号触发函数
        # 清除cookie
        self.browser.delete_all_cookies()
        # 关闭浏览器
        self.browser.quit()

    def start_requests(self):
        url = 'https://app.adspy.com/login'
        data = {'uname': '8428792@qq.com', 'upwd': 'Leite1999'}
        yield scrapy.Request(url, callback=self.parse, meta=data, dont_filter=True)

    def parse(self, response):
        if response.status == 200:
            html = etree.HTML(response.body.decode('utf-8'))
            bodys = html.xpath('//div[@class="ad-outer-box"]')
            try:
                for body in bodys:
                    table = body.xpath('.//table[@width="100%"]')
                    # FB视频预览地址
                    pageviewUrl = table[0].xpath('.//td[4]/a[2]/@href') if table else ''
                    page_list = pageviewUrl[0].split('/') if pageviewUrl else ''
                    if page_list:
                        item = fb_video_Item()
                        # 主页ids
                        item['pageId'] = page_list[-3]
                        yield item
            except Exception as e:
                self.spider.exception(e)
            else:
                self.loggers.info("登陆成功，解析完毕!")
        else:
            self.loggers.info("登录失败！")
