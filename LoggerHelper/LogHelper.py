import os
import time
import datetime
import logging
from logging import Handler, FileHandler, StreamHandler

# 日志级别关系映射
level_relations = {
    'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING,
    'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL
    }

class PathFileHandler(FileHandler):
    def __init__(self, path, filename, mode='a', encoding=None, delay=False):
        # 判断文件目录是否存在
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                file_path = os.path.join(path, filename)
                if not os.path.exists(file_path):
                    f = open(file_path, 'w')
                    f.close()
        except :
            pass
        try:
            del self.baseFilename
        except:
            pass
        self.baseFilename = os.path.join(path, filename)
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        if delay:
            Handler.__init__(self)
            self.stream = None
        else:
            StreamHandler.__init__(self, self._open())





class LoggersHelper(object):
    def __init__(self, log_level, filename):
        self.level = log_level
        self.log_file_path = self.get_file_path()
        self.file_name = filename
        self.date = time.strftime("%Y-%m-%d",time.localtime())

    def get_file_path(self):
        # 日志保存路径
        to_day = datetime.datetime.now()
        log_file_path = "log/scrapy_{}_{}_{}".format(to_day.year,to_day.month,to_day.day)
        return log_file_path


    def Loggers(self):
        self.logger = logging.getLogger(self.filename())
        # 设置日志级别
        self.logger.setLevel(level_relations.get(self.level))
        # 设置日志格式
        self.log_fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        self.format_str = logging.Formatter(self.log_fmt)
        # 往屏幕上输出
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.format_str)
        # 往文件输出
        self.file_handler = PathFileHandler(path = self.path(), filename = self.filename(), mode = 'a')
        self.file_handler.setFormatter(self.format_str)
        # 设置输出方式
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)
        return self.logger

    def NewLoggers(self):
        # 更改日志保存目录
        localtime = time.strftime("%Y-%m-%d",time.localtime())
        day1 = datetime.datetime.strptime(localtime, '%Y-%m-%d')
        day2 = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        delday = day1 - day2
        if delday.days == 1:
            # 删除原有的handler
            self.logger.removeHandler(self.file_handler)
            # 往文件输出
            self.file_handler = PathFileHandler(path=self.path(), filename=self.filename(), mode='a')
            self.file_handler.setFormatter(self.format_str)
            # 设置输出方式
            self.logger.addHandler(self.file_handler)
            self.date = localtime
        return self.logger



    def path(self):
        # 日志保存路径
        to_day = datetime.datetime.now()
        abspath = os.path.dirname(os.path.abspath(__file__))
        abspath = '/'.join(abspath.split('/')[:-1])
        self.log_file_path = self.get_file_path()
        file_path = os.path.join(abspath, self.log_file_path)
        return file_path

    def filename(self):
        # 文件名
        to_day = datetime.datetime.now()
        filename = "{}_{}_{}_{}.log".format(self.file_name, to_day.year, to_day.month, to_day.day)
        return filename



if __name__ == "__main__":
    txt = "hello world"
    log = Loggers(level = LOG_LEVEL, directory = path, filename = 'manager2.log')
    log.logger.info(4)
    log.logger.info(5)
    log.logger.info(txt)