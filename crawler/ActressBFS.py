import threading
import time
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.TimeoutUtil import TimeoutUtil
from utils.AttrsUtil import AttrsUtil
from utils.ActressUtil import ActressUtil
from utils.WebUtil import WebUtil
from utils.exceptions.PageException import PageException


class actresses:
    webUtil = WebUtil()
    actressUtil = ActressUtil()
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    requestUtil = RequestUtil()
    vos = []
    starUrl = ""
    pageNum = 1
    baseUrl = ""
    lock = threading.Lock()
    pageUtil = None
    timeoutUtil = TimeoutUtil()

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.pageUtil = PageUtil(url)
        self.isCensored = is_censored

    def BFS(self):
        star_time = time.time()
        while True:
            if self.isCensored:
                link = self.baseUrl + "actresses/" + str(self.pageNum)
            else:
                link = self.baseUrl + "uncensored/actresses/" + str(self.pageNum)
            source = self.webUtil.getWebSite(link)
            self.logUtil.log("now page num is " + str(self.pageNum))
            bs = BeautifulSoup(source, "html.parser")
            if self.pageUtil.hasNextPage(bs):
                try:
                    self.__bfs(source)
                except PageException:
                    self.pageUtil.save2local(source, link, ".html")
            else:
                self.logUtil.log("final page is reach")
                try:
                    self.__bfs(source)
                except PageException:
                    self.pageUtil.save2local(source, link, ".html")
                break
            self.pageNum += 1
        end_time = time.time()
        self.logUtil.log("bfs done")
        self.logUtil.log("thread running time is " + str(end_time - star_time))
        if not self.timeoutUtil.isEmpty():
            self.timeoutUtil.requestTimeoutLink()

    def __bfs(self, source):
        if not source:
            return
        actressList = []
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                actress_dict = self.attrsUtil.getSingleActressLink(brick)
                if actress_dict:
                    try:
                        actress = self.actressUtil.getActressDetails(
                            actress_dict["actress_link"]
                        )
                    except Exception as e:
                        self.save2local(
                            source,
                            threading.currentThread().getName() + "__bfs",
                            ".html",
                        )
                    if actress:
                        if not self.actressUtil.matchLinkIsCompanyLink(
                            actress_dict["photo_link"]
                        ):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                actress.photo_link = url + actress.photo_link
                        actress.actress_link = actress_dict["actress_link"]
                        actress.is_censored = self.isCensored
                        actressList.append(actress.toDict())
                else:
                    self.save2local(
                        source, threading.currentThread().getName() + "__bfs", ".html"
                    )
            self.requestUtil.send(actressList, "/actress/save")
        else:
            self.logUtil.log("bricks not found")

    def printActresses(self, actress):
        with actresses.lock:
            self.logUtil.log("info of " + actress.name + " was collected")
            self.logUtil.log(
                "----------------actress info start-----------------------------"
            )
            self.logUtil.log(actress)
            self.logUtil.log(
                "----------------actress info over-----------------------------"
            )
