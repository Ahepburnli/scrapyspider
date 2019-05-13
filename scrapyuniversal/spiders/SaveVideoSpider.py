# encoding:utf-8

import scrapy
import json
from scrapyuniversal.items.Fb_Download_Item import fb_download_Item
import sys
import os
import datetime
import random
from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler

from scrapyuniversal.settings import FB_VIDEO_CONTENT_URL # url保存在redis数据库中的键名

from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_SAVEVIDEO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT



class SaveVideoSpider(scrapy.Spider):
    name = "saveVideoSpider"
    allowed_domains = ['facebook.com']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'text/html;charset=utf-8',
            'referer': 'https://www.facebook.com/',
            },
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.SaveVideoPipeline.SaveVideoPipeline': 100,
            },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapyuniversal.middlewares.RandomUserAgentMiddleware.RandomUserAgentMiddleware': 100,
            },
        #抓捕403异常
        'HTTPERROR_ALLOWED_CODES': [403],
        #'DOWNLOAD_DELAY': random.random() * 2,
        # The initial download delay
        'AUTOTHROTTLE_START_DELAY': 0.01,
        # The maximum download delay to be set in case of high latencies
        'AUTOTHROTTLE_MAX_DELAY': 0.1,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        }

    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_SAVEVIDEO)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("启动SaveVideoSpider，准备开始工作...")
        super(SaveVideoSpider, self).__init__()



    def start_requests(self):
        while self.client_redis.exists(FB_VIDEO_CONTENT_URL):
            try:
                data = self.client_redis.spop(FB_VIDEO_CONTENT_URL)
                if not data:
                    continue
                data = json.loads(data.decode('utf-8'))
                item = fb_download_Item()
                try:
                    item['videoId'] = data['videoId']
                except:
                    item['pageId'] = data['pageId']
                url = ''  #
                if 'videoImg' in data.keys():
                    url = data['videoImg']

                    item['videoImg'] = data['videoImg']
                elif 'originVideoUrl' in data.keys():
                    url = data['originVideoUrl']

                    item['originVideoUrl'] = data['originVideoUrl']
                elif 'originRadio' in data.keys():
                    url = data['originRadio']

                    item['originRadio'] = data['originRadio']
                elif 'originalLogoSrc' in data.keys():
                    url = data['originalLogoSrc']

                    item['originalLogoSrc'] = data['originalLogoSrc']
                if url:
                    yield scrapy.Request(url,callback=self.parse,meta={'item':item},dont_filter=True)  # 此位置爬取图片链接时会出现ERROR: Missing scheme in request url，url需改为列表
                else:
                    self.loggers.info("error,url为：" + url)
            except Exception as e:
                self.loggers.exception(e)

    def parse(self, response):
        item = response.meta['item']
        if response.status == 200:
            item['file_content'] = response.body
        else:
            item['file_content'] = None
            self.loggers.info("爬取失败: " + response.url)
        yield item