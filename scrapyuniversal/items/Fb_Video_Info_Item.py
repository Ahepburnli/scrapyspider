
from scrapy import Field, Item


class fb_video_info_Item(Item):
    #视频id
    videoId = Field()
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