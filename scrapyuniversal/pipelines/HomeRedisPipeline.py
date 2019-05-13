

import json
from scrapyuniversal.settings import HOMEPAGE_DATA

class HomeRedisPipeline():
    '''
        将数据保存到Mysql数据库
    '''
    def process_item(self, item, spider):
        data = json.dumps(dict(item),ensure_ascii=False)
        spider.client_redis.lpush(HOMEPAGE_DATA,data)
        return item