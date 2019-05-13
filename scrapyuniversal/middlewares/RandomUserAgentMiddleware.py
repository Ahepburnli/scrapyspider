
import random

class RandomUserAgentMiddleware(object):
    '''
    这个类主要用于产生随机User-Agent
    '''
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        #从settings.py中加载USER_AGENTS的值
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self,request,spider):
        #在process_request中设置User-Agent的值
        request.headers['User-Agent'] = random.choice(self.agents)