

class Request:
    """请求(内容)"""

    def __init__(self, reason):
        self.__reason = reason
        self.__leader = None

    def getReason(self):
        return self.__reason