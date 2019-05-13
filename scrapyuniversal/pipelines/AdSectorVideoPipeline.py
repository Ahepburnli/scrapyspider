import hashlib

import json

from scrapyuniversal.settings import VIDEO_DATA
from scrapyuniversal.settings import VIDEO_INFO_DATA




class AdSectorVideoPipeline(object):
    '''
        将数据保存到redis数据库
    '''
    def process_item(self, item, spider):
        item_keys = dict(item).keys()
        try:
            if 'videoId' in item_keys:
                data = json.dumps(dict(item), ensure_ascii=False)
                spider.client_redis.lpush(VIDEO_DATA, data)
            return item
        except Exception as e:
            spider.loggers.exception(e)


    def finger_print(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data.encode('utf-8')).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger
