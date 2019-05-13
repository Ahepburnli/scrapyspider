# -*- coding: utf-8 -*-
import scrapy
import time
import sys
import os
from scrapy.exceptions import CloseSpider
from scrapyuniversal.items.Fb_Homepage_Item import fb_homepage_Item

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.xlib.pydispatch import dispatcher  # 信号分发器
from scrapy import signals  # 信号

from scrapyuniversal.settings import FB_HOMEPAGE_URL  # url保存在redis数据库中的键名

from scrapyuniversal.settings import LOG_LEVEL  # 日志等级
from scrapyuniversal.settings import NAME_HOMEPAGE
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT
import datetime


class HomepageSpider(scrapy.Spider):
    name = 'homepageSpider'
    allowed_domains = ['facebook.com']
    start_urls = []

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'referer': 'https://www.facebook.com',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.facebook.com',
            'Host': 'www.facebook.com',
        },
        'SELENIUM_TIMEOUT': 30,
        'LOAD_IMAGE': True,
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.HomeRedisPipeline.HomeRedisPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapyuniversal.middlewares.HomeChromeMiddleware': 100,
        },
        # 'DOWNLOAD_DELAY': random.random() * 2,
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
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_HOMEPAGE)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("启动HomepageSpider，准备开始工作...")
        super(HomepageSpider, self).__init__()

    def start_requests(self):
        # 设置spider爬取的次数，以防触发反爬，以600次为宜
        num = 0
        while self.client_redis.exists(FB_HOMEPAGE_URL) and num < 3:
            try:
                url = self.client_redis.rpop(FB_HOMEPAGE_URL)
                if not url:
                    self.loggers.info("主页链接有误！")
                    continue
                url = url.decode('utf-8')
                yield scrapy.Request(url, callback=self.parse, meta={'url': url})
                num += 1
            except Exception as e:
                self.loggers.exception(e)

    def parse(self, response):
        if response.status == 200:
            item = fb_homepage_Item()
            # 主页id
            pageId = response.xpath('.').re('"pageID":"(\d*?)"')
            item['pageId'] = pageId[0] if pageId else ''
            # 主页名称
            pageName = response.xpath('.').re('"name":"([\s\S]*?)"')
            item['pageName'] = pageName[0] if pageName else ''
            if pageId and item['pageName'] == '\\u963f\\u8054\\u914b\\u8fea\\u62c9\\u59c6':
                # facebook启动反爬，此处将链接放回，并退出spider
                self.client_redis.rpush(FB_HOMEPAGE_URL, response.request.url)
                self.loggers.info(response.url + ": facebook禁止访问")
                raise CloseSpider(reason="facebook禁止访问")
            # 主页地址
            item['url'] = response.url
            # adspy.com获取到的主页id转换成主页名链接
            page_id = response.request.meta['url'].split('/')
            page_id = page_id[-1] if page_id[-1] else page_id[-2]
            item['page_name'] = response.url if page_id == item['pageId'] else ''
            # 主页logo链接
            originalLogoSrc = response.xpath('.').re('"usernameEditDialogProfilePictureURI":"([\s\S]*?)"')
            try:
                item['originalLogoSrc'] = originalLogoSrc[0].replace('\/', '/')
            except Exception as e:
                item['originalLogoSrc'] = ''
            # 是否下载Logo，0-未下载,1-下载
            item['isDownload'] = 0
            # 主页对应商店地址
            shopUrl = response.xpath('.').re('"website_url":"([\s\S]*?)"')
            try:
                item['shopUrl'] = shopUrl[0].replace('\/', '/')
            except Exception as e:
                item['shopUrl'] = ''
            # 主页点赞次数
            likeCount1 = response.xpath('.').re(
                'yLtEhZl0QOJ.png"[\s\S]*?<div class="_4bl9"><div>([\s\S]*?) people like this</div>')
            likeCount2 = response.xpath('.').re(
                'yLtEhZl0QOJ.png"[\s\S]*?<div class="_4bl9"><div>([\s\S]*?) 位用户赞了</div>')
            likeCount = likeCount1 if likeCount1 else likeCount2
            likeCount = likeCount[0] if likeCount else '0'
            if ',' in likeCount:
                item['likeCount'] = int(''.join(likeCount.split(',')))
            else:
                item['likeCount'] = int(likeCount)
            # 粉丝数
            fansCount1 = response.xpath('.').re(
                'dsGlZIZMa30.png"[\s\S]*?<div class="_4bl9"><div>([\s\S]*?) people follow this</div>')
            fansCount2 = response.xpath('.').re(
                'dsGlZIZMa30.png"[\s\S]*?<div class="_4bl9"><div>([\s\S]*?) 位用户关注了</div>')
            fansCount = fansCount1 if fansCount1 else fansCount2
            fansCount = fansCount[0] if fansCount else '0'
            if ',' in fansCount:
                item['fansCount'] = int(''.join(fansCount.split(',')))
            else:
                item['fansCount'] = int(fansCount)
            # 主页类别
            category = response.xpath('.').re('</i><a href="/pages/category/[\s\S]*?/[\s\S]*?">([\s\S]*?)</a>')
            item['category'] = ' '.join(category) if category else ''
            # 主页状态,pageId为空，登录限制
            item['status'] = 30 if pageId else 0
            # 最近更新时间
            item['lastUpdateDate'] = int(time.time())
            item['cate_id'] = 0
            self.loggers.info(response.url + ": 爬取成功！")
            yield item
        else:
            self.loggers.info(response.url + " 状态码异常: " + response.status)
