from bs4 import BeautifulSoup
from crawler.utils.RequestUtil import RequestUtil

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

    def __init__(self, url) -> None:
        self.baseUrl = url
        self.starUrl = self.baseUrl + "/actresses"

    def BFS(self):
        while self.pageNum <= 3:
            source = self.webUtil.getWebSite(self.starUrl)
            print("现在正在第" + str(self.pageNum) + "页")
            self.__bfs(source)
            self.pageNum += 1
        print("bfs done")

    def __bfs(self, source):
        stars = []
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                star_dict = self.attrsUtil.getSingleStarLink(brick)
                star = self.starUtil.getStarDetails(star_dict["star_link"])
                if not "pics.dmm.co.jp" in star_dict["photo_link"]:
                    if self.baseUrl.endswith("/"):
                        url = self.baseUrl[:-1]
                        star.photo_link = url + star.photo_link
                    else:
                        star.photo_link = self.baseUrl + star.photo_link
                star.star_link = star_dict["star_link"]
                print("info of " + star.name + " was collected")
                print("----------------star info start-----------------------------")
                print(star.toDict())
                print("----------------star info over-----------------------------")
                stars.append(star.toDict())
            self.send({"is_censored": True, "stars": stars}, "star/relation/censor")

        else:
            print("bricks not found")

    def send(self, data, path):
        response = self.requestUtil.post(data=data, path=path)
        if response.status_code == 200:
            print("send data to " + path + " was success")
        else:
            print("send data to " + path + " was failure")
