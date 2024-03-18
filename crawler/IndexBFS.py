import hashlib
import threading
import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil

from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.exceptions.PageException import PageException


class index:
    webUtil = WebUtil()
    pageUtil = None
    logUtil = LogUtil()
    links = []
    pageNum = 1
    baseUrl = ""
    timeouts = []
    isCensored = True
    lock = threading.Lock()

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.pageUtil = PageUtil(url)
        self.isCensored = is_censored

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
                        try:
                            isFinalPage = False
                            while not isFinalPage:
                                isFinalPage = self.pageUtil.parseMovieListPage(
                                    link, self.isCensored
                                )
                        except PageException:
                            self.pageUtil.save2local(source, link, ".html")
                    else:
                        self.logUtil.log("final page is reach")
                        try:
                            self.__bfs(source)
                        except PageException:
                            self.pageUtil.save2local(source, link, ".html")
                        break
                else:
                    self.logUtil.log("request page timeout try next page")
                self.pageNum += 1
            end_time = time.time()
            self.logUtil.log("bfs done")
            self.logUtil.log("thread running time is " + str(end_time - star_time))

    def sendData2Server(self, page):
        if not page:
            self.logUtil.log("page is none")
            return
        if page.movie and len(page.movie) >= 1:
            self.requestUtil.send(page.movie, "/movie/save")
        if page.bigimage and len(page.bigimage) >= 1:
            movieBigImageVo = {
                "movie": page.movie,
                "bigImage": page.bigimage,
            }
            self.requestUtil.send(movieBigImageVo, "/movie/relation/bigimage/save")
        if page.categories and len(page.categories) >= 1:
            movieCategoryVo = {"movie": page.movie, "categories": page.categories}
            self.requestUtil.send(movieCategoryVo, "/movie/relation/category/save")
        if page.director and len(page.director) >= 1:
            movieDirectVo = {"movie": page.movie, "director": page.director}
            self.requestUtil.send(movieDirectVo, "/movie/relation/director/save")
        if page.label and len(page.label) >= 1:
            movieLabelVo = {"movie": page.movie, "label": page.label}
            self.requestUtil.send(movieLabelVo, "/movie/relation/label/save")
        if page.sampleimage and len(page.sampleimage) >= 1:
            movieSampleImageVo = {"movie": page.movie, "sampleImages": page.sampleimage}
            self.requestUtil.send(
                movieSampleImageVo, "/movie/relation/sampleimage/save"
            )
        if page.actresses and len(page.actresses) >= 1:
            if page.director:
                starDirectorVo = {"actress": page.actresses, "director": page.director}
                self.requestUtil.send(starDirectorVo, "/actress/relation/director/save")
            if page.studio:
                starStudioVo = {"actress": page.actresses, "studio": page.studio}
                self.requestUtil.send(starStudioVo, "/actress/relation/studio/save")
            if page.series:
                starSeriesVo = {"actress": page.actresses, "series": page.series}
                self.requestUtil.send(starSeriesVo, "/actress/relation/series/save")
            if page.movie:
                movieActressVo = {"movie": page.movie, "actress": page.actresses}
                self.requestUtil.send(movieActressVo, "/movie/relation/actress/save")
            if page.categories and len(page.categories) >= 1:
                starCategoryVo = {
                    "actress": page.actresses,
                    "categories": page.categories,
                }
                self.requestUtil.send(starCategoryVo, "/actress/relation/category/save")
        if page.studio and len(page.studio) >= 1:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.requestUtil.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series and len(page.series) >= 1:
            movieSeriesVo = {"movie": page.movie, "series": page.series}
            self.requestUtil.send(movieSeriesVo, "/movie/relation/series/save")

    def printPage(self, page):
        with index.lock:
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
