
class Person:
    """请求者(请假人)"""

    def __init__(self):
        self.__leader = None

    def setLeader(self, leader):
        self.__leader = leader

    def getLeader(self):
        return self.__leader

    def sendReuqest(self, request):
        print("事由：%s" % (request.getReason()))
        if (self.__leader is not None):
            self.__leader.handleRequest(request)