# -*- coding: utf-8 -*-
import scrapy
import time
import random
from scrapyuniversal.items.Fb_Video_Info_Item import fb_video_info_Item
import sys
import os

from scrapyuniversal.settings import FB_VIDEO_INFO_URL # url保存在redis数据库中的键名

import datetime

from scrapyuniversal.settings import LOG_LEVEL # 日志等级
from scrapyuniversal.settings import NAME_VIDEO_INFO
from scrapyuniversal.settings import CLIENT_HOST
from scrapyuniversal.settings import CLIENT_DB
from scrapyuniversal.settings import CLIENT_PASSWORD
from scrapyuniversal.settings import CLIENT_PORT

from LoggerHelper.LogHelper import LoggersHelper
from RedisHelper.RedisHelper import RedisHandler


class VideoInfoSpider(scrapy.Spider):
    name = 'videoInfoSpider'
    allowed_domains = ['facebook.com']
    start_urls = ['http://www.facebook.com/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding':'text/html;charset=utf-8',
            'referer':'https://www.facebook.com/',
             },
        'ITEM_PIPELINES': {
            'scrapyuniversal.pipelines.VideoInfoTextPipeline.VideoInfoTextPipeline': 90,
            'scrapyuniversal.pipelines.VideoInfoRedisPipeline.VideoInfoRedisPipeline': 100,
            },
        'DOWNLOADER_MIDDLEWARES': {
           'scrapyuniversal.middlewares.RandomUserAgentMiddleware.RandomUserAgentMiddleware': 543,
            },
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
        super(VideoInfoSpider, self).__init__()
        # 创建日志对象
        self.loggershelper = LoggersHelper(LOG_LEVEL, NAME_VIDEO_INFO)
        self.loggers = self.loggershelper.Loggers()
        self.loggers.info("启动VideoInfoSpider，准备开始工作...")


    def start_requests(self):
        self.loggers.info("爬取中...")
        while self.client_redis.exists(FB_VIDEO_INFO_URL):
            try:
                url = self.client_redis.spop(FB_VIDEO_INFO_URL)
                if not url:
                    continue
                yield scrapy.Request(url.decode('utf-8'),callback=self.parse,method='POST')
            except Exception as e:
                self.loggers.exception(e)


    def parse(self, response):
        if response.status == 200:
            item = fb_video_info_Item()
            #视频id
            video = response.url.split('/')
            item['videoId']= video[-1] if video[-1] else video[-2]
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
            if views or likes or comments or shares:
                self.loggers.info(response.url+ ": 爬取成功")
                yield item
            else:
                self.loggers.info(response.url + ": 爬取失败")
        else:
            self.loggers.info(response.url + "状态码异常，爬取失败！")

