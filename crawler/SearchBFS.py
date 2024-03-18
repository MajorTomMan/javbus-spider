import threading
import time

from bs4 import BeautifulSoup
from utils.ActressUtil import ActressUtil
from utils.LogUtil import LogUtil
from utils.TimeoutUtil import TimeoutUtil
from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.AttrsUtil import AttrsUtil


class search:
    webUtil = WebUtil()
    pageUtil = None
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    links = []
    pageNum = 1
    searchUrl = ""
    isCensored = True
    tag = ""
    timeouts = []
    lock = threading.Lock()
    actressUtil = ActressUtil()
    timeoutUtil = None

    def __init__(self, url, tag, is_censored):
        self.baseUrl = url
        self.pageUtil = PageUtil(url)
        self.isCensored = is_censored
        self.tag = tag
        self.timeoutUtil = TimeoutUtil(self.pageUtil)

    def BFS(self):
        if self.baseUrl:
            star_time = time.time()
            while True:
                if self.isCensored:
                    link = (
                        self.baseUrl
                        + "searchstar/"
                        + self.tag
                        + "/"
                        + str(self.pageNum)
                    )
                source = self.webUtil.getWebSite(link)
                if source:
                    self.logUtil.log("now page num is " + str(self.pageNum))
                    bs = BeautifulSoup(source, "html.parser")
                    if self.pageUtil.hasNextPage(bs):
                        self.__bfs(source)
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

    # 处理女优搜索结果页的BFS
    def __bfs(self, source):
        if not source:
            return
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                isCensored = self.attrsUtil.getIsCensored(brick)
                link = self.attrsUtil.getLink(brick)
                if link:
                    self.logUtil.log("now visit website link is " + link)
                    self.links.append(link)
                    isFinalPage = False
                    pageNum = 0
                    while not isFinalPage:
                        pageNum += 1
                        isFinalPage = self.pageUtil.parseMovieListPage(
                            link + "/" + str(pageNum), isCensored
                        )
            self.logUtil.log("all link was visited jump to next page")

        else:
            self.logUtil.log("bricks not found")
