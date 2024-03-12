import time
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.RequestUtil import RequestUtil

from utils.AttrsUtil import AttrsUtil
from utils.StarUtil import StarUtil
from utils.WebUtil import WebUtil


class stars:
    webUtil = WebUtil()
    starUtil = StarUtil()
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
        while self.pageNum <= 3:
            if self.isCensored:
                url = self.baseUrl + "actresses/" + str(self.pageNum)
            else:
                url = self.baseUrl + "uncensored/actresses/" + str(self.pageNum)
            source = self.webUtil.getWebSite(url)
            self.logUtil.log("现在正在第" + str(self.pageNum) + "页")
            self.__bfs(source)
            self.pageNum += 1
        end_time = time.time()
        self.logUtil.log("bfs done")
        self.logUtil.log("thread running time is " + str(end_time - star_time))

    def __bfs(self, source):
        if not source:
            return
        stars = []
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                star_dict = self.attrsUtil.getSingleStarLink(brick)
                star = self.starUtil.getStarDetails(star_dict["star_link"])
                if star:
                    if not self.starUtil.matchLinkIsCompanyLink(
                        star_dict["photo_link"]
                    ):
                        if self.baseUrl.endswith("/"):
                            url = self.baseUrl[:-1]
                            star.photo_link = url + star.photo_link
                    star.star_link = star_dict["star_link"]
                    star.is_censored = self.isCensored
                    self.logUtil.log("info of " + star.name + " was collected")
                    self.logUtil.log(
                        "----------------star info start-----------------------------"
                    )
                    self.logUtil.log(star.toDict())
                    self.logUtil.log(
                        "----------------star info over-----------------------------"
                    )
                    stars.append(star.toDict())
                else:
                    self.timeouts.append(
                        {"name": star_dict["name"], "link": star_dict["star_link"]}
                    )
                    self.logUtil.log(
                        "request "
                        + star_dict["name"]
                        + ":"
                        + star_dict["star_link"]
                        + " timeout  add it to timeouts"
                    )
            self.send(stars, "/star/save")
            if self.timeouts and len(self.timeouts) >= 1:
                self.logUtil.log("try to request timeout list")
                for link in self.timeouts:
                    star = self.starUtil.getStarDetails(link)
                    if star:
                        if self.starUtil.matchLinkIsCompanyLink(
                            star_dict["photo_link"]
                        ):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                star.photo_link = url + star.photo_link
                            else:
                                star.photo_link = self.baseUrl + star.photo_link
                        star.star_link = link
                        self.send(
                            {"stars": stars},
                            "/star/save",
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
