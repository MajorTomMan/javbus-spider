import time
from bs4 import BeautifulSoup
from utils.RequestUtil import RequestUtil

from utils.AttrsUtil import AttrsUtil
from utils.StarUtil import StarUtil
from utils.WebUtil import WebUtil


class stars:
    vos = []
    starUrl = ""
    pageNum = 1
    webUtil = WebUtil()
    starUtil = StarUtil()
    attrsUtil = AttrsUtil()
    baseUrl = ""
    requestUtil = RequestUtil()
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
            print("现在正在第" + str(self.pageNum) + "页")
            self.__bfs(source)
            self.pageNum += 1
        print("bfs done")

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
                    print("info of " + star.name + " was collected")
                    print(
                        "----------------star info start-----------------------------"
                    )
                    print(star.toDict())
                    print("----------------star info over-----------------------------")
                    stars.append(star.toDict())
                else:
                    self.timeouts.append(
                        {"name": star_dict["name"], "link": star_dict["star_link"]}
                    )
                    print(
                        "request "
                        + star_dict["name"]
                        + ":"
                        + star_dict["star_link"]
                        + " timeout  add it to timeouts"
                    )
            self.send(stars, "/star/save")
            if self.timeouts and len(self.timeouts) >= 1:
                print("try to request timeout list")
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
                        print(
                            "retry "
                            + self.timeouts["name"]
                            + self.timeouts["link"]
                            + " was success"
                        )
                    else:
                        print(
                            "retry "
                            + self.timeouts["name"]
                            + self.timeouts["link"]
                            + " was failure name abandon"
                        )
        else:
            print("bricks not found")

    def send(self, data, path):
        response = self.requestUtil.post(data=data, path=path)
        if not response:
            print("request not response pls check server is open or has expection ")
        elif response.status_code == 200:
            print("send data to " + path + " was success")
        else:
            print("send data to " + path + " was failure")
