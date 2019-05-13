from scrapy import Field, Item

class fb_cookie_Item(Item):
    #cookie
    cookies = Field()
    #cookie对应的用户名
    uname = Field()
    #uname对应的标志
    flag = Field()
    #cookie对应的标志
    cookie_flag = Field()
