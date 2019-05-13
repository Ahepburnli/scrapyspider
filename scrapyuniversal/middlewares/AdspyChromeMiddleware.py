
import random
import json
import time
import re

from selenium.common.exceptions import TimeoutException,UnableToSetCookieException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from scrapy.exceptions import CloseSpider

from scrapyuniversal.settings import ADSPY_SELECT_URL


class AdspyChromeMiddleware(object):
    def process_request(self, request, spider):
        """
        用Chrome抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        if request.meta.get('uname', None):
            #清除历史cookie
            spider.browser.delete_all_cookies()
            name = request.meta['uname']
            password = request.meta['upwd']
            try:
                #登录facebook
                spider.browser.get(request.url)
                #用户名登录框是否出现
                wait = WebDriverWait(spider.browser, 10)
                wait.until(EC.presence_of_element_located((By.NAME, 'userName')))
                email = spider.browser.find_element_by_name('userName')
                email.clear()
                email.send_keys(name)
                #密码登录框是否出现
                wait = WebDriverWait(spider.browser, 10)
                wait.until(EC.presence_of_element_located((By.NAME, 'password')))
                pd = spider.browser.find_element_by_name('password')
                pd.clear()
                pd.send_keys(password)
                loginbutton = spider.browser.find_element_by_xpath('//button[@type="submit"]')
                loginbutton.send_keys(Keys.ENTER)
                #显示等待10s
                wait = WebDriverWait(spider.browser, 10)
                wait.until(EC.presence_of_element_located((By.ID, 'filters')))
                spider.loggers.info(name + ": 登录成功！")
                # 开始查询...
                spider.browser.get(ADSPY_SELECT_URL)
                #滑到底部
                spider.loggers.info("开始下拉翻页获取视频链接...")
                for i in range(0,200000,10000):
                    time.sleep(3)
                    spider.loggers.info("第" + str(i // 10000 + 1) + '次翻页...')
                    spider.browser.execute_script("window.scrollBy(0," + str(10000) + ")")
                time.sleep(5)
                return HtmlResponse(url=request.url, body=spider.browser.page_source,
                                    request=request, encoding='utf-8',status=200)
            except TimeoutException:
                spider.loggers.info(name + " : 等待超时！")
                return HtmlResponse(url=request.url, status=404, request=request)
        else:
            try:
                #访问其他链接
                spider.loggers.info("正在获取视频详情...")
                spider.browser.get(request.url)
                #显示等待10s
                wait = WebDriverWait(spider.browser, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ad-outer-box')))
                spider.loggers.info(request.url + ": 视频信息获取成功!")
                return HtmlResponse(url=request.url, body=spider.browser.page_source,
                                    request=request, encoding='utf-8',status=200)
            except TimeoutException:
                spider.loggers.info(request.url + ": 等待超时！")
                return HtmlResponse(url=request.url, status=404, request=request)

