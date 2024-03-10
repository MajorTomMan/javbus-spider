from utils.WebUtil import WebUtil


class proxypool:
    webUtil = WebUtil()
    links = []
    baseUrl = "https://www.bing.com/search?q=代理免费Ip"

    def getPageList(self):
        response = self.webUtil.get(self.baseUrl)
        if response:
            print()
