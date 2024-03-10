import json

from bs4 import BeautifulSoup

from utils.PageUtil import PageUtil
from utils.WebUtil import WebUtil
from utils.RequestUtil import RequestUtil
from utils.AttrsUtil import AttrsUtil


class search:
    webUtil = WebUtil()
    pageUtil = None
    attrsUtil = AttrsUtil()
    requestUtil = RequestUtil()
    links = []
    pageNum = 1
    searchUrl = ""
    isCensored = True

    def __init__(self, url, tag, is_censored):
        if is_censored == True:
            self.searchUrl = url + "search/" + tag + "/" + str(self.pageNum)
        else:
            self.searchUrl = (
                url + "uncensored/" + "search/" + tag + "/" + str(self.pageNum)
            )
        self.pageUtil = PageUtil(url)
        self.isCensored = is_censored

    def BFS(self):
        if self.searchUrl:
            while self.pageNum <= 5:
                source = self.webUtil.getWebSite(self.baseUrl)
                if source:
                    bs = BeautifulSoup(source, "html.parser")
                    ul = bs.find("ul", {"class": "pagination pagination-lg"})
                    if ul:
                        self.__bfs(source)
                    else:
                        print("final page is reach")
                        self.__bfs(source)
                        break
                else:
                    print("request page timeout try next page")
                self.pageNum += 1
            print("bfs done")

    def __bfs(self, source):
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.attrsUtil.getLink(brick)
                if link:
                    print("now visit website link is " + link)
                    self.links.append(link)
                    try:
                        page = self.pageUtil.parseDetailPage(link)
                    except Exception as e:
                        print(e)
                    page.movie.is_censored = self.isCensored
                    # self.save2local(page.toDict(), "./page/data")
                    if page and page != -1:
                        print(
                            "------------------------------page info start--------------------------------------"
                        )
                        print(page)
                        print(
                            "------------------------------page info ended--------------------------------------"
                        )
                        if page.stars:
                            print(
                                "------------------------------star info start--------------------------------------"
                            )
                            for star in page.stars:
                                print("star: " + str(star))
                            print(
                                "------------------------------star info ended--------------------------------------"
                            )
                        self.sendData2Server(page=page)
                    elif page == -1:
                        continue
                    else:
                        print("add " + link + " to timeouts")
                        self.timeouts.append(link)
            if not self.timeouts and len(self.timeouts) >= 1:
                for link in self.timeouts:
                    print("try to request failed link")
                    print("now visit website link is " + link)
                    page = self.pageUtil.parseDetailPage(link)
                    if page:
                        print(
                            "------------------------------page info start--------------------------------------"
                        )
                        print(page)
                        print(
                            "------------------------------page info ended--------------------------------------"
                        )
                        if page.stars:
                            print(
                                "------------------------------star info start--------------------------------------"
                            )
                            for star in page.stars:
                                print("star: " + str(star))
                            print(
                                "------------------------------star info ended--------------------------------------"
                            )
                        self.sendData2Server(page)
                        print("request " + link + " success")
                    else:
                        print("request " + link + " failed  link abandon")
            print("all link was visited jump to next page")
        else:
            print("page list not found")

    def save2local(self, content, path):
        with open(path + ".json", "w+", encoding="UTF-8") as f:
            json.dump(content, f, ensure_ascii=False)

    def send(self, data, path):
        response = self.requestUtil.post(data=data, path=path)
        if not response:
            print("request not response pls check server is open or has expection ")
        elif response.status_code == 200:
            print("send data to " + path + " was success")
        else:
            print("send data to " + path + " was failure")

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
        if page.stars and len(page.stars) >= 1:
            if page.director:
                starDirectorVo = {"stars": page.stars, "director": page.director}
                self.send(starDirectorVo, "/star/relation/director/save")
            if page.studio:
                starStudioVo = {"stars": page.stars, "studio": page.studio}
                self.send(starStudioVo, "/star/relation/studio/save")
            if page.series:
                starSeriesVo = {"stars": page.stars, "series": page.series}
                self.send(starSeriesVo, "/star/relation/series/save")
            if page.movie:
                movieStarVo = {"movie": page.movie, "stars": page.stars}
                self.send(movieStarVo, "/movie/relation/star/save")
            if page.categories and len(page.categories) >= 1:
                starCategoryVo = {"stars": page.stars, "categories": page.categories}
                self.send(starCategoryVo, "/star/relation/category/save")
        if page.studio and len(page.studio) >= 1:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series and len(page.series) >= 1:
            movieSeriesVo = {"movie": page.movie, "series": page.series}
            self.send(movieSeriesVo, "/movie/relation/series/save")
