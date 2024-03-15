from asyncio import timeouts
import json
import threading
import time

from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil

from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.RequestUtil import RequestUtil
from utils.AttrsUtil import AttrsUtil


class index:
    webUtil = WebUtil()
    pageUtil = None
    attrsUtil = AttrsUtil()
    requestUtil = RequestUtil()
    logUtil = LogUtil()
    links = []
    pageNum = 1
    baseUrl = ""
    timeouts = []
    isCensored = True
    lock = threading.Lock()

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.pageUtil = PageUtil(url, is_censored)
        self.isCensored = is_censored
        self.baseUrls = self.webUtil.baseUrls

    def BFS(self):
        if self.baseUrl:
            star_time = time.time()
            while True:
                if self.isCensored:
                    source = self.webUtil.getWebSite(
                        self.baseUrl + "page/" + str(self.pageNum)
                    )
                else:
                    source = self.webUtil.getWebSite(
                        self.baseUrl + "uncensored/page/" + str(self.pageNum)
                    )
                if source:
                    bs = BeautifulSoup(source, "html.parser")
                    self.logUtil.log("now page num is " + str(self.pageNum))
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

    def __bfs(self, source):
        if not source:
            return

        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.attrsUtil.getLink(brick)
                if link:
                    self.logUtil.log("now visit website link is " + link)
                    self.links.append(link)
                    page = None
                    try:
                        page = self.pageUtil.parseDetailPage(
                            link,
                        )
                    except Exception as e:
                        self.logUtil.log(e)
                    # self.save2local(page.toDict(), "./page/data")
                    with index.lock:
                        if page and page != -1:
                            page.movie["is_censored"] = self.isCensored
                            self.logUtil.log(
                                "------------------------------page info start--------------------------------------"
                            )
                            self.logUtil.log(page)
                            self.logUtil.log(
                                "------------------------------page info ended--------------------------------------"
                            )
                            if page.actresses:
                                self.logUtil.log(
                                    "------------------------------actress info start--------------------------------------"
                                )
                                for actress in page.actresses:
                                    self.logUtil.log(actress)
                                self.logUtil.log(
                                    "------------------------------actress info ended--------------------------------------"
                                )
                        elif page == -1:
                            continue
                        else:
                            self.logUtil.log("add " + link + " to timeouts")
                            self.timeouts.append(link)
                    self.sendData2Server(page=page)
            if self.timeouts and len(self.timeouts) >= 1:
                for link in self.timeouts:
                    self.logUtil.log("try to request failed link")
                    self.logUtil.log("now visit website link is " + link)
                    page = self.pageUtil.parseDetailPage(link)
                    if page:
                        self.logUtil.log(
                            "------------------------------page info start--------------------------------------"
                        )
                        self.logUtil.log(page)
                        self.logUtil.log(
                            "------------------------------page info ended--------------------------------------"
                        )
                        self.sendData2Server(page)
                        self.logUtil.log("request " + link + " success")
                    else:
                        self.logUtil.log("request " + link + " failed  link abandon")
            self.logUtil.log("all link was visited jump to next page")
        else:
            self.logUtil.log("page list not found")

    def save2local(self, content, path):
        with open(path + ".json", "w+", encoding="UTF-8") as f:
            json.dump(content, f, ensure_ascii=False)

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

    def sendData2Server(self, page):
        if page.movie and len(page.movie) >= 1:
            self.send(page.movie, "/movie/save")
        if page.bigimage and len(page.bigimage) >= 1:
            movieBigImageVo = {
                "movie": page.movie,
                "bigImage": page.bigimage,
            }
            self.send(movieBigImageVo, "/movie/relation/bigimage/save")
        if page.categories and len(page.categories) >= 1:
            movieCategoryVo = {"movie": page.movie, "categories": page.categories}
            self.send(movieCategoryVo, "/movie/relation/category/save")
        if page.director and len(page.director) >= 1:
            movieDirectVo = {"movie": page.movie, "director": page.director}
            self.send(movieDirectVo, "/movie/relation/director/save")
        if page.label and len(page.label) >= 1:
            movieLabelVo = {"movie": page.movie, "label": page.label}
            self.send(movieLabelVo, "/movie/relation/label/save")
        if page.sampleimage and len(page.sampleimage) >= 1:
            movieSampleImageVo = {"movie": page.movie, "sampleImages": page.sampleimage}
            self.send(movieSampleImageVo, "/movie/relation/sampleimage/save")
        if page.actresses and len(page.actresses) >= 1:
            if page.director:
                starDirectorVo = {"actress": page.actresses, "director": page.director}
                self.send(starDirectorVo, "/actress/relation/director/save")
            if page.studio:
                starStudioVo = {"actress": page.actresses, "studio": page.studio}
                self.send(starStudioVo, "/actress/relation/studio/save")
            if page.series:
                starSeriesVo = {"actress": page.actresses, "series": page.series}
                self.send(starSeriesVo, "/actress/relation/series/save")
            if page.movie:
                movieActressVo = {"movie": page.movie, "actress": page.actresses}
                self.send(movieActressVo, "/movie/relation/actress/save")
            if page.categories and len(page.categories) >= 1:
                starCategoryVo = {
                    "actress": page.actresses,
                    "categories": page.categories,
                }
                self.send(starCategoryVo, "/actress/relation/category/save")
        if page.studio and len(page.studio) >= 1:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series and len(page.series) >= 1:
            movieSeriesVo = {"movie": page.movie, "series": page.series}
            self.send(movieSeriesVo, "/movie/relation/series/save")
