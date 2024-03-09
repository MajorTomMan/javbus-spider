import json
import orjson
from bs4 import BeautifulSoup
from utils.Utils import AttrsUtil, PageUtil, WebUtil, RequestUtil


class index:
    WebUtil = WebUtil()
    PageUtil
    AttrsUtil = AttrsUtil()
    RequestUtil = RequestUtil()
    links = []
    pageNum = 1
    baseUrl = ""

    def __init__(self, url):
        self.baseUrl = url + "page/" + str(self.pageNum)
        self.PageUtil = PageUtil(url)

    def BFS(self):
        if self.baseUrl:
            while self.pageNum <= 5:
                driver = self.WebUtil.getWebSite(self.baseUrl)
                print("现在正在第" + str(self.pageNum) + "页")
                if self.WebUtil.checkisLimitedByAge(driver.title):
                    return
                self.__bfs(driver)
                break
            print("bfs done")

    def __bfs(self, driver):
        bs = BeautifulSoup(driver.page_source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.AttrsUtil.getLink(brick)
                if link:
                    print("now visit website link is " + link)
                    self.links.append(link)
                    page = self.PageUtil.parseDetailPage(link)
                    self.save2local(page.toDict(), "./page/data")
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
                        self.sendData2Server(page=page)

            print("all link was visited jump to next page")
        else:
            print("page list not found")

    def save2local(self, content, path):
        with open(path + ".json", "w", encoding="UTF-8") as f:
            json.dump(content, f, ensure_ascii=False)

    def send(self, data, path):
        response = self.RequestUtil.post(data=data, path=path)
        if response.status_code == 200:
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
            movieStarVo = {"movie": page.movie, "stars": page.stars}
            starCategoryVo = {"stars": page.stars, "categories": page.categories}
            starDirectorVo = {"stars": page.stars, "director": page.director}
            starStudioVo = {"stars": page.stars, "studio": page.studio}
            starSeriesVo = {"stars": page.stars, "series": page.series}
            self.send(movieStarVo, "/movie/relation/star/save")
            self.send(starCategoryVo, "/star/relation/category/save")
            self.send(starDirectorVo, "/star/relation/director/save")
            self.send(starStudioVo, "/star/relation/studio/save")
            self.send(starSeriesVo, "/star/relation/series/save")
        if page.studio and len(page.studio) >= 1:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series and len(page.series) >= 1:
            movieSeriesVo = {"movie": page.movie, "studio": page.series}
            self.send(movieSeriesVo, "/movie/relation/series/save")
