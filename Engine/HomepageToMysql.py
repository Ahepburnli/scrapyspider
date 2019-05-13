from BaseObserver import Observer
from SpiderServer import SpiderServer

import json
import hashlib

# HomepageSpider爬取到的数据保存在redis
from settings import HOMEPAGE_DATA


class HomepageToMysql(Observer):
    '''
    该模式用于保存数据
    功能：保存主页信息，并更新fb_items表状态
    '''

    def __init__(self, server_redis, client_redis, logger, dbhelper):
        super().__init__()
        # 创建连接server_redis本地端redis
        self.server_redis = server_redis
        self.client_redis = client_redis
        self.logger = logger
        self.dbhelper = dbhelper

    def storeHomepage(self, data):
        data = json.loads(data.decode('utf-8'))
        # 更新fb_items表中主页链接状态
        self.updateItems(data)
        # 如果status为0，则不放入数据库
        if not data['status']:
            return
        # 删除page_name,用于adspy.com更新fb_items
        page_name = data['page_name']
        del data['page_name']
        try:
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert ignore into %s (%s) values (%s)' % ('fb_homepage', keys, values)
            result = self.dbhelper.insert(sql, tuple(data.values()))
        except Exception as e:
            self.logger.exception(e)
        # 更新fb_items表
        if page_name and result:
            self.storeItems(page_name)
        # 插入失败，改为更新数据
        if not result:
            try:
                # 检查originalLogoSrc是否有变动
                sql = "select logoSrc from fb_homepage where originalLogoSrc=%s" % data['originalLogoSrc']
                flag = self.dbhelper.select(sql)
                if bool(flag):
                    del data['originalLogoSrc']
                    del data['isDownload']
                # 不更新status的值
                del data['status']
                s = []
                for key, value in data.items():
                    s.append(key + '="' + str(value) + '"')
                s = ','.join(s)
                sql = 'update %s set %s where pageId="%s"' % ('fb_homepage', s, data['pageId'])
                self.dbhelper.insert(sql)
            except Exception as e:
                self.logger.exception(e)

    def updateItems(self, data):
        if not data:
            return
        try:
            status = data.get("status", None)
            if not status:
                # 如果status为0，则将fb_items表的status减1
                sql = "update fb_items set status=IF(status<=0, 0, status-1) WHERE url='%s'" % data['url']
            else:
                # 如果status大于0，则将fb_items表的status加1
                sql = "update fb_items set status=IF(status>=30, 30, status+1) WHERE url='%s'" % data['url']
            self.dbhelper.insert(sql)
        except Exception as e:
            self.logger.exception(e)

    def storeItems(self, data):
        '''
        保存主页url链接
        '''
        if not data:
            return
        try:
            # 指纹打码，redis中取值为bytes类型
            code = self.fingerPrint(data.encode('utf-8'))
            url = data
            status = 30
            sql = "insert ignore into fb_items(url,code,status) values('%s','%s','%s')" % (url, code, status)
            self.dbhelper.insert(sql)
        except Exception as e:
            self.logger.exception(e)

    def fingerPrint(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger

    def update(self, observable, object):
        if isinstance(observable, SpiderServer) \
                and observable.getMessage() == HOMEPAGE_DATA:
            data = self.server_redis.rpop(HOMEPAGE_DATA)
            if not data:
                return
            self.storeHomepage(data)
            self.logger.info("保存 %s 完毕！" % HOMEPAGE_DATA)
