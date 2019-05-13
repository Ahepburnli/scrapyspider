import datetime

#视频预览图、视频、音频、logo保存路径
IMAGES_STORE = 'source/logo/'
VIDEO_STORE = 'source/video/'
VIDEOIMG_STORE = 'source/videoImg/'
AUDIO_STORE = 'source/audio/'


#===========fb_items================
#启动HomepageSpider需要的主页url
ITEMS_URL = 'url'
#url保存在redis数据库中的键名
FB_HOMEPAGE_URL = 'fb_homepage_url'
#HomepageSpider爬取到的数据保存在redis
HOMEPAGE_DATA = 'homepage_data'
#===========fb_homepage=============
#启动VideoSpider需要的主页url
VIDEO_ADS_URL = 'url'
#url保存在redis数据库中的键名--videoSpider
FB_VIDEO_ADS_URL = 'fb_video_ads_url'
#url保存在redis数据库中的键名--videoSpider
FB_LOCAL_VIDEO_ADS_URL = 'fb_local_video_ads_url'
#VideoSpider爬取到的数据保存在redis
VIDEO_DATA = 'video_data'
#===========fb_video==================
#启动SaveVideoSpider需要的视频、视频首帧图、音频下载url
VIDEOIMG = 'videoImg'
ORIGINVIDEOURL = 'originVideoUrl'
ORIGINRADIO = 'originRadio'
#url保存在redis数据库中的键名
FB_VIDEO_CONTENT_URL = 'fb_video_content_url'
#SaveVideoSpider爬取到的数据保存在redis
VIDEO_CONTENT_DATA = 'video_content_data'
#从fb_homepage中获取主页originalLogoSrc
ORIGINALLOGOSRC = 'originalLogoSrc'
#===========fb_video==================
#启动VideoInfoSpider需要的url
PAGEVIEWURL = 'pageviewUrl'
#url保存在redis数据库中的键名
FB_VIDEO_INFO_URL = 'fb_video_info_url'
#VideoInfoSpider爬取到的数据保存在redis
VIDEO_INFO_DATA = 'video_info_data'
#===========fb_user_cookie========
#保存在redis中的账户信息
FB_ACCOUNTS = 'accounts:facebook'
#===========fb_user_cookie===============
#fb_user_cookie表中所有的cookies
FB_COOKIES = 'cookies:facebook'
#loginspider登录后获取到的cookie保存在redis
COOKIES_DATA = 'cookies_data'
#将验证通过的cookies保存在reids
TEST_COOKIES_DATA = 'test_cookies_data'
#本地videoSpider使用的cookies，保存在本地redis
SPIDER_COOKIES = 'cookies:spider'
#===============================
# adSector.com网站、facebook网站爬取到的视频预览地址，用于解析视频详情信息
ADS_VIDEO = 'ads_video'



# 信息指令,用于请求数据
# 请求账户
REFRESH_ACCOUNTS = 'refresh_accounts'
# 请求cookie
REFRESH_COOKIES = "refresh_cookies"
# 请求所有
REFRESH_ALL = "refresh_all"
# 请求视频、音频、图片下载链接
REFRESH_VIDEO_CONTENT = "refresh_video_content"
# 请求主页链接
REFRESH_HOMEPAGE = "refresh_homepage"
# 请求主页logo下载链接
REFRESH_LOGOSRC = "refresh_logoSrc"
# 请求主页链接，用于获取信息与广告，供爬虫子节点使用
REFRESH_ADS = "refresh_ads"
# 请求视频预览链接
REFRESH_INFO = "refresh_info"




# 日志级别
LOG_LEVEL = 'INFO'
# 日志文件名
FILENAME = 'manager'


#配置连接本地server端redis
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6379
SERVER_DB = 0
SERVER_PASSWORD = 'Leite012068'

#配置连接远程客户端redis
CLIENT_HOST = '127.0.0.1'
CLIENT_PORT = 6379
CLIENT_DB = 0
CLIENT_PASSWORD = 'Leite012068'


#MYSQL连接设置
MYSQL_HOST = '204.12.207.146'
MYSQL_PORT = 3306
MYSQL_USER = 'fbuser'
MYSQL_PWD = 'leite9988'
MYSQL_DB = 'facebook'
MYSQL_CHARSET = 'utf8mb4'
