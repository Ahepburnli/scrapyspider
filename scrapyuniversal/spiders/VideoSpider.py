# -*- coding: utf-8 -*-
import time
import re
import scrapy
import json
import random


from scrapyuniversal.items.Fb_Video_Item import fb_video_Item
from lxml import etree
import sys
import os
from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler


from scrapyuniversal.settings import FB_VIDEO_ADS_URL # url保存在redis数据库中的键名

from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_VIDEO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT


import datetime

class VideoSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = 'videoSpider'
    allowed_domains = ['facebook.com']
    start_urls = ['https://adsector.com/login']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'referer':'https://www.facebook.com',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'Host': 'www.facebook.com',
             },
        'DOWNLOADER_MIDDLEWARES': {
            #'scrapyuniversal.middlewares.AdSectorChromeMiddleware': 120,
            },
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.VideoRedisPipeline.VideoRedisPipeline': 34,
            },
        # 抓捕500异常
        'HTTPERROR_ALLOWED_CODES': [500],
        #是否启动重试
        'RETRY_ENABLED': False,
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
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_VIDEO)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("VideoSpider启动...")
        super(VideoSpider, self).__init__()


    def start_requests(self):
        # 设置spider爬取的次数，以防触发反爬，以600次为宜
        root_url = "https://www.facebook.com/pages/ads/more/?page_id=%s&cursor=0&surface=www_page_ads&unit_count=16&country=1&__a=1"
        while self.client_redis.exists(FB_VIDEO_ADS_URL):
            try:
                data = self.client_redis.rpop(FB_VIDEO_ADS_URL)
                if not data:
                    self.loggers.info("主页id有误！")
                    continue
                pageId_url = json.loads(data.decode('utf-8'))
                pageId = pageId_url['pageId']
                pageUrl = pageId_url['url']
                url = root_url % pageId
                yield scrapy.Request(url,callback=self.parse, meta={'pageUrl': pageUrl})
            except Exception as e:
                self.loggers.exception(e)



    def parse(self, response):
        if response.status == 200:
            #"video_url":"\/EpochTimesTrending\/videos\/370567580452385\/",
            video_urls = response.xpath('.').re('"video_url":"([\s\S]*?)",')
            if video_urls:
                self.loggers.info(response.url + " : 解析到%d个视频！" % len(video_urls))
                for video_url in video_urls:
                    video_url = "https://www.facebook.com" + video_url.replace('\/', '/')
                    item = fb_video_Item()
                    item['pageviewUrl'] = video_url
                    yield item
            # 没有广告视频
            else:
                item = fb_video_Item()
                item['pageUrl'] = response.request.meta['pageUrl']
                self.loggers.info(response.url + " : 没有视频广告！")
                yield item
        else:
            self.loggers.info(response.url + "状态码异常： " + str(response.status))
