from scrapy import Field, Item

class fb_download_Item(Item):
    '''
    用于下载视频、图片、音频
    '''
    #视频id
    videoId = Field()
    #主页id
    pageId = Field()
    #视频首帧图
    videoImg = Field()
    #视频下载地址
    originVideoUrl = Field()
    #音频下载地址
    originRadio = Field()
    #logo下载地址
    originalLogoSrc = Field()
    #内容
    file_content = Field()
    #文件名
    file_name = Field()
    #最近更新时间
    lastUpdateDate = Field()
    # 服务器保存地址
    videoUrl = Field()
    # 音频保存服务器地址
    radioUrl = Field()
    # 视频首帧图保存服务器地址
    imgSrc = Field()
    # logo服务器地址
    logoSrc = Field()
    #是否下载,0-未下载,1-下载
    isDownload = Field()