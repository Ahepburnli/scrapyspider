

class ForbiddenSpiderError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('facebook禁止访问')

