# -*- coding: utf-8 -*-

# Scrapy settings for scrapyuniversal project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import random
import datetime
import os
import time

BOT_NAME = 'scrapyuniversal'

SPIDER_MODULES = ['scrapyuniversal.spiders']
NEWSPIDER_MODULE = 'scrapyuniversal.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyuniversal (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = random.random() * 10
#DOWNLOAD_DELAY = 30
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 6

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
#   'Accept-Encoding':'gzip, deflate, br',
# }
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
]


# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'scrapyuniversal.middlewares.RandomUserAgentMiddleware.RandomUserAgentMiddleware': 543,
}

DOWNLOAD_FAIL_ON_DATALOSS = False
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'scrapy_redis.pipelines.RedisPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#视频预览图、视频、音频、logo保存路径
IMAGES_STORE = 'source/logo/'
VIDEO_STORE = 'source/video/'
VIDEOIMG_STORE = 'source/videoImg/'
AUDIO_STORE = 'source/audio/'

#本地videoSpider使用的cookies，保存在本地redis
SPIDER_COOKIES = 'cookies:spider'
#fb_user_cookie表中所有的cookies
FB_COOKIES = 'cookies:facebook'
#用于爬取video广告的url保存在redis数据库中的键名
FB_VIDEO_ADS_URL = 'fb_video_ads_url'
#url保存在redis数据库中的键名--videoSpider
FB_LOCAL_VIDEO_ADS_URL = 'fb_local_video_ads_url'
#保存在redis中的账户信息
FB_USER_DATA = 'accounts:facebook'
#广告的视频、音频、图片的url保存在redis数据库中的键名
FB_VIDEO_CONTENT_URL = 'fb_video_content_url'
#主页url保存在redis数据库中的键名
FB_HOMEPAGE_URL = 'fb_homepage_url'
#从fb_homepage中获取主页originalLogoSrc
ORIGINALLOGOSRC = 'originalLogoSrc'
#广告视频的url保存在redis数据库中的键名
FB_VIDEO_INFO_URL = 'fb_video_info_url'


# Cookie分数
MIN_SCORE = 0
MAX_SCORE = 3

#===========fb_items================
#HomepageSpider爬取到的数据保存在redis
HOMEPAGE_DATA = 'homepage_data'
#===========fb_homepage=============
#VideoSpider爬取到的数据保存在redis
VIDEO_DATA = 'video_data'
#===========fb_video==================
#SaveVideoSpider爬取到的数据保存在redis
VIDEO_CONTENT_DATA = 'video_content_data'
#===========fb_video==================
#VideoInfoSpider爬取到的数据保存在redis
VIDEO_INFO_DATA = 'video_info_data'
#===========fb_cookies================
#将登陆成功后获取cookies保存在reids
COOKIES_DATA = 'cookies_data'
#将验证通过的cookies保存在reids
TEST_COOKIES_DATA = 'test_cookies_data'
#===============================
# adSector.com网站、facebook网站爬取到的视频预览地址，用于解析视频详情信息
ADS_VIDEO = 'ads_video'


# 爬取adspy.com网站需要的查询条件
ADSPY_SELECT_URL = 'https://app.adspy.com/ads;siteType=Facebook;mediaType=Video;tech=%EF%BC%BB350%EF%BC%BD;countries=%EF%BC%BB%22US%22%EF%BC%BD'
# 爬取adspy.com网站获取到的主页URL
ADSPY_HOMEPAGE_URL = 'adspy_homepage_url'
# 爬取adSector.com网站需要的查询条件
today = datetime.date.today().strftime("%Y-%m-%d")
yesterday = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%Y-%m-%d")
ADSECTOR_SELECT_URL = 'https://adsector.com/search?date={}%20-%20{}&dateMode=hit&country[]=US&type[]=video&ecommerce[]=1'.format(yesterday,today)

#启用“Ajax可抓取页面”的抓取
AJAXCRAWL_ENABLED = True


# 启用logging
#LOG_ENABLED = False
# Scrapy日志有五种等级，按照范围递增顺序排列如下
#CRITICAL - 严重错误
#ERROR - 一般错误
#WARNING - 警告信息
#INFO - 一般信息
#DEBUG - 调试信息

LOG_LEVEL = 'DEBUG'
# logging使用的编码
#LOG_ENCODING = 'utf-8'
# 在当前目录里创建logging输出文件的文件名
#LOG_FILE = log_file_path
# videoinfo日志文件名
NAME_VIDEO_INFO = 'videoinfo'
NAME_HOMEPAGE = 'homepage'
NAME_SAVEVIDEO = 'savevideo'
NAME_ADSPYSPIDER = 'adspySpider'
NAME_POSTSPIDER = 'postSpider'
NAME_ADSECTOR = 'adSector'
NAME_ADSVIDEO = 'adsvideo'
NAME_VIDEO = 'video'


# 信息指令
REFRESH_ACCOUNTS = 'refresh_accounts'
REFRESH_COOKIES = "refresh_cookies"
REFRESH_ALL = "refresh_all"
REFRESH_VIDEO_CONTENT = "refresh_video_content"
REFRESH_HOMEPAGE = "refresh_homepage"
REFRESH_LOGOSRC = "refresh_logoSrc"
REFRESH_ADS = "refresh_ads"
REFRESH_LOCAL_ADS = "refresh_local_ads"
REFRESH_INFO = "refresh_info"



#配置连接远程客户端redis
CLIENT_HOST = '127.0.0.1'
CLIENT_PORT = 6379
CLIENT_DB = 0
CLIENT_PASSWORD = 'Leite012068'