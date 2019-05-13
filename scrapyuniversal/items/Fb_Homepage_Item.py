from scrapy import Field, Item

class fb_homepage_Item(Item):
    #主页id
    pageId = Field()
    #主页名称
    pageName= Field()
    #主页地址
    url= Field()
    #主页logo
    originalLogoSrc= Field()
    #服务器保存logo地址
    logoSrc= Field()
    #是否下载logo
    isDownload= Field()
    #主页对应商店地址
    shopUrl= Field()
    #主页点赞次数
    likeCount= Field()
    #粉丝数
    fansCount= Field()
    #主页类别
    category= Field()
    #主页状态
    status= Field()
    #更新时间
    lastUpdateDate= Field()
    #主页分类信息，默认为0
    cate_id = Field()
    # 用于adspy网站获取到主页id转换成page_name
    page_name = Field()