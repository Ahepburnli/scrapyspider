from BaseObservable import Observable


class SpiderServer(Observable):
    """Spider服务器：负责任务调度"""

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.__message = ''

    def getMessage(self):
        return self.__message

    def setMessage(self, message):
        self.__message = message
        self.notifyObservers()