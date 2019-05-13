

import time


from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from scrapy.exceptions import CloseSpider


from scrapyuniversal.settings import ADSECTOR_SELECT_URL

import requests



class AdSectorChromeMiddleware(object):
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
                wait = WebDriverWait(spider.browser, 20)
                wait.until(EC.presence_of_element_located((By.NAME, 'login')))
                email = spider.browser.find_element_by_name('login')
                email.clear()
                email.send_keys(name)
                #密码登录框是否出现
                wait = WebDriverWait(spider.browser, 20)
                wait.until(EC.presence_of_element_located((By.NAME, 'password')))
                pd = spider.browser.find_element_by_name('password')
                pd.clear()
                pd.send_keys(password)
                loginbutton = spider.browser.find_element_by_xpath('//button[@type="submit"]')
                loginbutton.send_keys(Keys.ENTER)
                #显示等待10s
                wait = WebDriverWait(spider.browser, 20)
                wait.until(EC.presence_of_element_located((By.XPATH, '//select[@name="mode"]')))
                spider.loggers.info(name + ": 登录成功！")
                # 开始查询...
                spider.browser.get(ADSECTOR_SELECT_URL)
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
        elif request.meta.get('page', None):
            try:
                spider.browser.get(request.url)
                #显示等待10s
                wait = WebDriverWait(spider.browser, 20)
                wait.until(EC.presence_of_element_located((By.ID, 'content')))
                time.sleep(5)
                return HtmlResponse(url=request.url, body=spider.browser.page_source,
                                    request=request, encoding='utf-8',status=200)
            except TimeoutException:
                spider.loggers.info(request.url + ": 等待超时！")
                return HtmlResponse(url=request.url, status=404, request=request)
        else:
            # 读取数据
            html = requests.get(request.url)
            time.sleep(3)
            # 该响应返回给引擎，引擎交给spider进行解析
            response = HtmlResponse(url=request.url, body=html.content, request=request)
            return response