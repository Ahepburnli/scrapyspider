
import hashlib
import json

from scrapyuniversal.settings import VIDEO_DATA
from scrapyuniversal.settings import ADS_VIDEO



class VideoRedisPipeline(object):
    '''
        将数据保存到redis数据库
    '''
    def process_item(self, item, spider):
        item_keys = dict(item).keys()
        try:
            if 'pageUrl' in item_keys or 'videoId' in item_keys :
                data = json.dumps(dict(item), ensure_ascii=False)
                spider.client_redis.lpush(VIDEO_DATA, data)
            elif 'pageviewUrl' in item_keys and len(item_keys) == 1:
                url = item['pageviewUrl']
                finger = self.finger_print(url)
                # 去重，主页url唯一
                flag = spider.client_redis.sismember(ADS_VIDEO + "_set", finger)
                if not flag:
                    spider.client_redis.rpush(ADS_VIDEO, url)
                    spider.client_redis.sadd(ADS_VIDEO + "_set", finger)
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
