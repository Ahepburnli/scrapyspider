import json
from scrapyuniversal.settings import VIDEO_INFO_DATA


class VideoInfoRedisPipeline():
    '''
        将数据保存到Redis数据库
    '''
    def process_item(self, item, spider):
        data = json.dumps(dict(item),ensure_ascii=False)
        spider.client_redis.lpush(VIDEO_INFO_DATA,data)
        return item
