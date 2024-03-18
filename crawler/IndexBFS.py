import time
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil

from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.TimeoutUtil import TimeoutUtil


class index:
    webUtil = WebUtil()
    pageUtil = None
    logUtil = LogUtil()
    links = []
    pageNum = 1
    baseUrl = ""
    isCensored = True
    timeoutUtil = None

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.pageUtil = PageUtil(url)
        self.isCensored = is_censored
        self.timeoutUtil = TimeoutUtil(self.pageUtil)

    def BFS(self):
        if self.baseUrl:
            star_time = time.time()
            while True:
                if self.isCensored:
                    link = self.baseUrl + "page/" + str(self.pageNum)
                else:
                    link = self.baseUrl + "uncensored/page/" + str(self.pageNum)
                source = self.webUtil.getWebSite(link)
                if source:
                    bs = BeautifulSoup(source, "html.parser")
                    self.logUtil.log("now page num is " + str(self.pageNum))
                    if self.pageUtil.hasNextPage(bs):
                        isFinalPage = False
                        while not isFinalPage:
                            isFinalPage = self.pageUtil.parseMovieListPage(
                                link, self.isCensored
                            )
                    else:
                        self.logUtil.log("final page is reach")
                        self.__bfs(source)
                        break
                else:
                    self.logUtil.log("request page timeout try next page")
                self.pageNum += 1
            end_time = time.time()
            self.logUtil.log("bfs done")
            self.logUtil.log("thread running time is " + str(end_time - star_time))
            if not self.timeoutUtil.isEmpty():
                self.timeoutUtil.requestTimeoutLink()
