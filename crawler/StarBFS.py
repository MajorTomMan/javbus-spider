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

    def __init__(self, url, is_censored) -> None:
        self.baseUrl = url
        if is_censored == True:
            self.starUrl = self.baseUrl + "actresses"
        else:
            self.starUrl = self.baseUrl + "uncensored/actresses"
        self.isCensored = is_censored

    def BFS(self):
        while self.pageNum <= 3:
            source = self.webUtil.getWebSite(self.starUrl)
            self.logUtil.log("现在正在第" + str(self.pageNum) + "页")
            self.__bfs(source)
            self.pageNum += 1
        self.logUtil.log("bfs done")

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
                    if not "pics.dmm.co.jp" in star_dict["photo_link"]:
                        if self.baseUrl.endswith("/"):
                            url = self.baseUrl[:-1]
                            star.photo_link = url + star.photo_link
                        else:
                            star.photo_link = self.baseUrl + star.photo_link
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
                        if not "pics.dmm.co.jp" in star_dict["photo_link"]:
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
