
from scrapy import Field, Item

class fb_video_Item(Item):
    #主页id
    pageId = Field()
    #标题
    title = Field()
    #视频id
    videoId = Field()
    #视频首帧图
    videoImg = Field()
    #FB视频地址
    originVideoUrl = Field()
    #音频地址
    originRadio = Field()
    #FB视频预览地址
    pageviewUrl = Field()
    #视频服务器保存地址
    videoUrl = Field()
    #视频发布时间
    publishDate = Field()
    #第一次爬取时间
    spiderDate = Field()
    #最近更新时间
    lastUpdateDate = Field()
    #视频介绍
    introduce = Field()
    #是否下载,0-未下载,1-下载
    isDownload = Field()
    #视频状态
    status = Field()
    # 音频保存服务器地址
    radioUrl = Field()
    # 视频首帧图保存服务器地址
    imgSrc = Field()
    # 广告地区
    countryId = Field()
    # 更新到主页对应的URL
    pageUrl = Field()
    # 广告商品链接
    landpage = Field()

    #浏览次数
    views = Field()
    #点赞数
    likes = Field()
    #评论数
    comments = Field()
    #分享数
    shares = Field()
    #最近更新时间
    lastupdate = Field()
    #视频发布时间
    publishDate = Field()
