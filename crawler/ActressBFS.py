import time
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.RequestUtil import RequestUtil

from utils.AttrsUtil import AttrsUtil
from utils.ActressUtil import ActressUtil
from utils.WebUtil import WebUtil


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
    timeouts = []
    isCensored = True

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.isCensored = is_censored

    def BFS(self):
        star_time = time.time()
        while True:
            if self.isCensored:
                url = self.baseUrl + "actresses/" + str(self.pageNum)
            else:
                url = self.baseUrl + "uncensored/actresses/" + str(self.pageNum)
            source = self.webUtil.getWebSite(url)
            self.logUtil.log("now page num is " + str(self.pageNum))
            bs = BeautifulSoup(source, "html.parser")
            ul = bs.find("ul", {"class": "pagination pagination-lg"})
            if ul:
                self.__bfs(source)
            else:
                self.logUtil.log("final page is reach")
                self.__bfs(source)
                break
            self.pageNum += 1
        end_time = time.time()
        self.logUtil.log("bfs done")
        self.logUtil.log("thread running time is " + str(end_time - star_time))

    def __bfs(self, source):
        if not source:
            return
        actresses = []
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                actress_dict = self.attrsUtil.getSingleActressLink(brick)
                actress = self.actressUtil.getActressDetails(
                    actress_dict["actress_link"]
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
                    self.logUtil.log("info of " + actress.name + " was collected")
                    self.logUtil.log(
                        "----------------actress info start-----------------------------"
                    )
                    self.logUtil.log(actress.toDict())
                    self.logUtil.log(
                        "----------------actress info over-----------------------------"
                    )
                    actresses.append(actress.toDict())
                else:
                    self.timeouts.append(
                        {
                            "name": actress_dict["name"],
                            "link": actress_dict["actress_link"],
                        }
                    )
                    self.logUtil.log(
                        "request "
                        + actress_dict["name"]
                        + ":"
                        + actress_dict["actress_link"]
                        + " timeout  add it to timeouts"
                    )
            self.send(actresses, "/actress/save")
            if self.timeouts and len(self.timeouts) >= 1:
                self.logUtil.log("try to request timeout list")
                for link in self.timeouts:
                    actress = self.actressUtil.getActressDetails(link)
                    if actress:
                        if self.actressUtil.matchLinkIsCompanyLink(
                            actress_dict["photo_link"]
                        ):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                actress.photo_link = url + actress.photo_link
                            else:
                                actress.photo_link = self.baseUrl + actress.photo_link
                        actress.actress_link = link
                        self.send(
                            {"actress": actresses},
                            "/actress/save",
                        )
                        self.logUtil.log(
                            "retry "
                            + self.timeouts["name"]
                            + self.timeouts["link"]
                            + " was success"
                        )
                    else:
                        self.logUtil.log(
                            "retry "
                            + self.timeouts["name"]
                            + self.timeouts["link"]
                            + " was failure name abandon"
                        )
        else:
            self.logUtil.log("bricks not found")

    def send(self, data, path):
        response = self.requestUtil.post(data=data, path=path)
        if not response:
            self.logUtil.log(
                "request not response pls check server is open or has expection "
            )
        elif response.status_code == 200:
            self.logUtil.log("send data to " + path + " was success")
        else:
            self.logUtil.log("send data to " + path + " was failure")
