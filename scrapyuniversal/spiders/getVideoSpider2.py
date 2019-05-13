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
from scrapyuniversal.settings import NAME_ADSVIDEO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT
from scrapyuniversal.settings import ADS_VIDEO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.xlib.pydispatch import dispatcher   # 信号分发器
from scrapy import signals                      # 信号


class GetVideoSpider(scrapy.Spider):
    handle_httpstatus_list = [404, 500]
    name = 'getVideoSpider2'
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
            'scrapyuniversal.pipelines.VideoInfoTextPipeline.VideoInfoTextPipeline': 90,
            'scrapyuniversal.pipelines.VideoRedisPipeline.VideoRedisPipeline': 100,
            },
        # 抓捕500异常
        'HTTPERROR_ALLOWED_CODES': [500],
        #是否启动重试
        'RETRY_ENABLED': False,
        #'DOWNLOAD_DELAY': random.random() * 2,
        # The initial download delay
        'AUTOTHROTTLE_START_DELAY': 5,
        # The maximum download delay to be set in case of high latencies
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        }

    def __init__(self):
        # 创建连接本地redis实例化对象
        self.client_redis = RedisHandler(CLIENT_HOST, CLIENT_PORT, CLIENT_DB, CLIENT_PASSWORD)
        self.client_redis.connectDataBase()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_ADSVIDEO)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("GetVideoSpider启动...")
        super(GetVideoSpider, self).__init__()


    def start_requests(self):
        # while self.client_redis.exists(ADS_VIDEO):
        #     url = self.client_redis.rpop(ADS_VIDEO)
        #     if url:
        #         yield scrapy.Request(url.decode('utf-8'),callback=self.parse)
        #     else:
        #         self.loggers.info("主页链接有误！")
        yield scrapy.Request('https://www.facebook.com/1942253219380826/videos/334492667109561',callback=self.parse)


    def parse(self, response):
        # 进入facebook.com视频展示页
        if response.status == 200:
            self.loggers.info(response.url + ": 开始解析视频...")
            # with open("facebook.html",'wb') as f:
            #     f.write(response.body)
            body = response.body.decode('utf-8')
            # 主页URL
            #str_contents = response.xpath(".").re('VideoDashPrefetchCache')
            str_contents = re.findall(r'VideoDashPrefetchCache', body)
            # 判断是否有广告视频
            if str_contents:
                item = fb_video_Item()
                # 解析视频详细信息
                pageId = re.findall(r'"page_id\\":(\d+?),',body)
                item['pageId'] = pageId[0] if pageId else ''
                videoId = response.url.split('/')
                item['videoId'] = videoId[-1] if videoId[-1] else videoId[-2]
                # 视频预览链接
                item['pageviewUrl'] = response.url
                # 提取发布日期
                publishDate = re.findall(r'"publish_time[\s\S]*?":(\d*?),',body)
                item['publishDate'] = publishDate[0] if publishDate else ''
                # 视频地址
                try:
                    originVideoUrl = re.findall(r',video:\[\{url:"([\s\S]*?)",',body)
                    if originVideoUrl:
                        originVideoUrl = ''.join(originVideoUrl[0].replace('\/', '/').split("amp;"))
                except Exception as e:
                    originVideoUrl = ''
                # 音频地址
                try:
                    originRadio = re.findall(r',audio:\[\{url:"([\s\S]*?)",',body)
                    if originRadio:
                        originRadio = ''.join(originRadio[0].replace('\/', '/').split("amp;"))
                except Exception as e:
                    originRadio = ''
                item['originVideoUrl'] = originVideoUrl if originVideoUrl else ''
                item['originRadio'] = originRadio if originRadio else ''
                # 提取title 、introduce
                introduce_info = re.findall(r'<div class="_5pbx userContent _3576"[\s\S]*?>([\s\S]*?)</div>',body)
                introduces = re.findall(r'>([\s\S]*?)<',introduce_info[0]) if introduce_info else ''
                introduce = ''.join(introduces) if introduces else ''
                title = introduces[0] if introduces else introduce
                item['title'] = title[:40] if title else ''
                item['introduce'] = introduce[:100] if introduce else ''
                # 提取视频的首帧图
                try:
                    videoImg = re.findall(r'<img class="_4lpf" src="([\s\S]*?)" />',body)
                    if not videoImg:
                        videoImg = re.findall(r'<img class="_3chq" src="([\s\S]*?)" />',body)
                    videoImg = ''.join(videoImg[0].replace('\/', '/').split("amp;")) if videoImg else ''
                except Exception as e:
                    self.loggers.exception(e)
                item['videoImg'] = videoImg if videoImg else ''
                # 视频下载日期
                item['spiderDate'] = int(time.time())
                # 视频最后下载日期
                item['lastUpdateDate'] = int(time.time())
                # 视频状态
                item['status'] = 1 if item['videoId'] else 0
                # 广告地区
                item['countryId'] = 1
                # 广告商品链接
                landpage = re.findall(r'<ul class="_53bj"><li><a href="([\s\S]*?)"',body)
                try:
                    landpage_url = urllib.parse.unquote(landpage[0]) if landpage else ''
                    landpage = landpage_url.split('u=')[-1] if landpage_url else ''
                    landpage = ''.join(landpage.split("amp;")) if landpage else ''
                    item['landpage'] = landpage if len(landpage) < 500 else ''
                except Exception as e:
                    self.loggers.exception(e)
                    item['landpage'] = ''
                # 解析视频评论、点赞、播放信息
                #浏览次数
                #video_view_count:null,
                views = response.xpath('.').re('video_view_count:(\d*?),')
                if not views:
                    views = response.xpath('.').re('viewCount:"([\s\S]*?)"')
                item['views'] = views[0] if views else '0'
                #点赞数
                #reaction_count:{count:9669},
                likes = response.xpath('.').re('reaction_count:\{count:(\d*?)\},')
                if not likes:
                    likes = response.xpath('.').re('likecount:(\d*?),')
                item['likes'] = likes[0] if likes else '0'
                #评论数
                # comment_count:{total_count:7}
                comments = response.xpath('.').re('comment_count:\{total_count:(\d*?)\},')
                if not comments:
                    comments = response.xpath('.').re('commentcount:(\d*?),')
                item['comments'] = comments[0] if comments else '0'
                #分享数
                #share_count:{count:65},share_count:{count:2628},
                shares = response.xpath('.').re('share_count:\{count:(\d*?)\},')
                if not shares:
                    shares = response.xpath('.').re('sharecount:(\d*?),')
                item['shares'] = shares[0] if shares else '0'
                #最近更新时间
                item['lastupdate'] = int(time.time())
                #视频发布日期
                publishDate = response.xpath('.').re('"publish_time[\s\S]*?":(\d*?),')
                item['publishDate'] = int(publishDate[0]) if publishDate else 0
                self.loggers.info(response.url+ ": 解析成功！")
                yield item
            elif re.findall(r'captcha_persist_data', body):
                self.loggers.info(response.url + ":需要安全验证！")
                self.client_redis.lpush(ADS_VIDEO, response.url)
            else:
                self.loggers.info(response.url + ": 解析失败！")