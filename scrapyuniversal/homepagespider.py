import os
import schedule
import time


def job():
    '''
    单独执行homeapgeSpider

    每6小时执行一次
    :return:
    '''
    os.system("scrapy crawl homepageSpider")


# schedule.every(360).minutes.do(job)
# 6小时执行一次
schedule.every(6).hours.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)