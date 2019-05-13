
import hashlib
import pickle
import time
import re
from scrapy.exceptions import DropItem

from scrapyuniversal.settings import AUDIO_STORE
from scrapyuniversal.settings import VIDEO_STORE
from scrapyuniversal.settings import VIDEOIMG_STORE
from scrapyuniversal.settings import IMAGES_STORE
from scrapyuniversal.settings import VIDEO_CONTENT_DATA


class SaveVideoPipeline(object):
    def process_item(self, item, spider):
        if 'videoImg' in dict(item).keys():
            name = re.findall(r'/([\s\S]*?)\?',item['videoImg'])
            name = name[0].split('/')[-1] if name else ''
            if not name and item['file_content']:
                finger = self.finger_print(item['file_content'])
                name = finger + '.jpg'
            item['imgSrc'] = VIDEOIMG_STORE + name if name else ''
            #item['isDownload'] = 1 if item['file_content'] else 2
        elif 'originVideoUrl' in dict(item).keys():
            name = re.findall(r'/([\s\S]*?)\?',item['originVideoUrl'])
            name = name[0].split('/')[-1] if name else ''
            if not name and item['file_content']:
                finger = self.finger_print(item['file_content'])
                name = finger + '.mp4'
            item['videoUrl'] = VIDEO_STORE + name if name else ''
            #以视频下载完成作为已下载标志
            item['isDownload'] = 1 if item['file_content'] else 4
            item['lastUpdateDate'] = int(time.time())
        elif 'originRadio' in dict(item).keys():
            name = re.findall(r'/([\s\S]*?)\?',item['originRadio'])
            name = name[0].split('/')[-1] if name else ''
            if not name and item['file_content']:
                finger = self.finger_print(item['file_content'])
                name = finger + '.mp4'
            item['radioUrl'] = AUDIO_STORE + name if name else ''
            #item['isDownload'] = 1 if item['file_content'] else 3
        elif 'originalLogoSrc' in dict(item).keys():
            name = re.findall(r'/([\s\S]*?)\?', item['originalLogoSrc'])
            name = name[0].split('/')[-1] if name else ''
            if not name and item['file_content']:
                finger = self.finger_print(item['file_content'])
                name = finger + '.jpg'
            item['logoSrc'] = IMAGES_STORE + name if name else ''
            item['isDownload'] = 1 if item['file_content'] else 4
        spider.client_redis.lpush(VIDEO_CONTENT_DATA,pickle.dumps(dict(item)))

    def finger_print(self, data):
        # 打码并进行判断
        if data:
            finger = hashlib.md5(data).hexdigest()
            # 将获取到的主页url放入到任务队列中
            return finger
