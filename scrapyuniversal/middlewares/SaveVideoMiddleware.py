import requests

class SaveVideoMiddleware(object):
    def process_request(self, request, spider):
        # 读取数据
        html = requests.get(request.url)
        # 该响应返回给引擎，引擎交给spider进行解析
        response = HtmlResponse(url=request.url, body=html.content, request=request)
        return response