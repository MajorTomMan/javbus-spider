import time
import random
import queue
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.AttrsUtil import AttrsUtil
from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.TimeoutUtil import TimeoutUtil
from utils.RequestUtil import RequestUtil

from collections import OrderedDict

visited = OrderedDict()
queue = queue.Queue()


class index:
    webUtil = WebUtil()
    pageUtil = None
    logUtil = LogUtil()
    links = []
    pageNum = 1
    baseUrl = ""
    isCensored = True
    timeoutUtil = None
    attrsUtil=AttrsUtil()
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
                    if self.pageUtil.hasNextPage(bs):
                        self.logUtil.log("now page num is " + str(self.pageNum))
                        self.bfs(bs)
                    else:
                        self.bfs(bs)
                        break
                else:
                    self.logUtil.log("request page timeout try next page")
                self.pageNum += 1
            end_time = time.time()
            self.logUtil.log("bfs done")
            self.logUtil.log("thread running time is " + str(end_time - star_time))
            if not self.timeoutUtil.isEmpty():
                self.timeoutUtil.requestTimeoutLink()

    def bfs(self, bs):
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.attrsUtil.getLink(brick)
                if link:
                    visited[link] = False
                    queue.put(link)
            while not queue.empty():
                link = queue.get()
                if not visited[link]:
                    visited[link]=True
                page = self.pageUtil.parseDetailPage(link,self.isCensored)
                if page and page!=-1:
                    self.pageUtil.sendData2Server(page)
                else:
                    return
                
        else:
            return

    def DFS(self, link):
        visited[link] = False
        self.dfs(link, 0)

    def dfs(self, link, depth):
        if visited[link] == True or depth >= 30:
            return
        visited[link] = True
        source = self.webUtil.getWebSite(link)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            if bs:
                page = self.pageUtil.parseDetailPage(bs, self.isCensored)
                if page:
                    self.pageUtil.sendData2Server(page)
                else:
                    pass
                related = bs.find("div", id="related-waterfall")
                links = self.pageUtil.findRelatedWebSite(related)
                if links and len(links) >= 1:
                    for link in links:
                        if link not in visited.keys():
                            visited[link] = False
                    link = self.randomChoiceOneLink()
                    if link:
                        self.dfs(link, depth + 1)
                    else:
                        return
                else:
                    return
            else:
                return
        else:
            return

    def randomChoiceOneLink(self):
        # 如果所有链接都已访问过，则返回 None 或采取其他适当的操作
        if all(visited.values()):
            return None

        # 从未访问过的链接中随机选择一个
        while True:
            link = random.choice(list(visited.keys()))
            if not visited[link]:
                return link
