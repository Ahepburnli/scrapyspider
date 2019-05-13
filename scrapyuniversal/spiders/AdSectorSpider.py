# -*- coding: utf-8 -*-
import scrapy
import time
import re
import os
import datetime
import random
import urllib
from scrapyuniversal.items.Fb_Video_Item import fb_video_Item
from scrapyuniversal.items.Fb_Video_Info_Item import fb_video_info_Item
from lxml import etree

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler

from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_ADSECTOR
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.xlib.pydispatch import dispatcher   # 信号分发器
from scrapy import signals                      # 信号


class AdSectorSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = 'adSectorSpider'
    allowed_domains = ['adsector.com','facebook.com']
    start_urls = ['https://adsector.com/login']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapyuniversal.middlewares.AdSectorChromeMiddleware.AdSectorChromeMiddleware': 120,
            },
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.AdSectorPageViewUrlPipeline.AdSectorPageViewUrlPipeline': 34,
            },
        # 抓捕500异常
        'HTTPERROR_ALLOWED_CODES': [500],
        #是否启动重试
        'RETRY_ENABLED': False,
        'DOWNLOAD_DELAY': random.random() * 2,
        # The initial download delay
        'AUTOTHROTTLE_START_DELAY': 0.01,
        # The maximum download delay to be set in case of high latencies
        'AUTOTHROTTLE_MAX_DELAY': 0.1,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_IP': 32,
        'DEPTH_LIMIT': 6,
        }

    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_ADSECTOR)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("AdSectorSpider启动...")
        #chrome无头版
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        # self.browser = webdriver.Chrome()
        # #浏览器窗口大小
        # self.browser.set_window_size(1400, 700)
        super(AdSectorSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self, spider):
        #信号触发函数
        #清除cookie
        self.browser.delete_all_cookies()
        #关闭浏览器
        self.browser.quit()

    def start_requests(self):
        url = 'https://adsector.com/login'
        data = {'uname':'leite2015','upwd':'Leite000'}
        yield scrapy.Request(url,callback=self.parse,meta=data,dont_filter=True)

    def parse(self, response):
        # 进入adSector.com
        if response.status == 200:
            self.loggers.info("登陆成功，开始解析...")
            html = response.body.decode('utf-8')
            html = etree.HTML(html)
            bodys = html.xpath('//ul[@class="items"]/li')
            for body in bodys:
                # 提取主页id
                pageUrl = body.xpath('.//div[@class="post--publisher ng-scope"]/a/@href')
                if pageUrl:
                    item = fb_video_Item()
                    item['pageId'] = pageUrl[0].split('/')[-1]
                    yield item
                # 提取视频广告详情链接
                ads_url = body.xpath('.//div[@class="post--media_wrap"]/a/@href')
                if ads_url:
                    url = "https://adsector.com" + ads_url[0]
                    yield scrapy.Request(url,callback=self.parse_page,meta ={'page':'page'},dont_filter=True)
            self.loggers.info(response.url + " : 解析完毕！")
        else:
            self.loggers.info("登录失败！")

    def parse_page(self, response):
        if response.status == 200:
            # 进入adSector.com详情页

            html = response.body.decode('utf-8')
            html = etree.HTML(html)
            video_url = html.xpath('//a[@ng-if="isAdvertisment"]/@href')
            if not video_url:
                video_url = response.xpath('//a[@ng-if="isAdvertisment"]/@href').extract()
            #https://facebook.com/442181916185819_792522581100393
            #https://www.facebook.com/442181916185819/videos/792522581100393/
            if video_url:
                try:
                    video_url = video_url[-1].split('/')[-1]
                    pageId, videoId = tuple(video_url.split('_'))
                    if pageId and videoId:
                        item = fb_video_Item()
                        url = "https://www.facebook.com/" + str(pageId) + '/videos/' + str(videoId)
                        item['pageviewUrl'] = url
                        yield item
                except Exception as e:
                    self.loggers.exception(e)
                else:
                    self.loggers.info(response.url + " 解析视频链接成功！")
            else:
                self.loggers.info(response.url + " 解析视频链接失败！")
