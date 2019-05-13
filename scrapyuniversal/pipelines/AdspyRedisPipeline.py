import hashlib

import json


from scrapyuniversal.settings import FB_HOMEPAGE_URL




class AdspyRedisPipeline(object):
    '''
        将数据保存到redis数据库
    '''
    def process_item(self, item, spider):
        try:
            url = 'https://www.facebook.com/' + item['pageId']
            finger = self.finger_print(url)
            # 将adspy.com网站爬取到的主页url放入adspy_homepage_url中
            # 将adSector网站爬取到的主页url放入adspy_homepage_url中
            # 去重，主页url唯一
            flag = spider.client_redis.sismember(FB_HOMEPAGE_URL + "_set", finger)
            if not flag:
                spider.client_redis.rpush(FB_HOMEPAGE_URL, url)
                spider.client_redis.sadd(FB_HOMEPAGE_URL + "_set", finger)
                spider.loggers.info("解析到新链接： " + url)
        except Exception as e:
            spider.loggers.exception(e)
        return item

    def finger_print(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode('utf-8')).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger
