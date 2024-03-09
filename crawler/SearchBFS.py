import json
from bs4 import BeautifulSoup
from utils.Utils import WebUtil, AttrsUtil, ImageUtil, PageUtil


class search:
    WebUtil = WebUtil()
    PageUtil
    AttrsUtil = AttrsUtil()
    links = []
    attrsList = []
    searchUrl = ""
    pageNum = 1

    def __init__(self, url, name) -> None:
        self.searchUrl = url + "/search/" + name + "/"
        self.PageUtil = PageUtil(url)

    # 默认是搜索模式
    def BFS(self):
        if self.baseUrl:
            while self.pageNum < 5:
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
        if page.movie:
            self.send(page.movie, "/movie/save")
        if page.bigimage:
            movieBigImageVo = {
                "movie": page.movie,
                "bigImage": page.bigimage,
            }
            self.send(movieBigImageVo, "/movie/relation/bigimage/save")
        if page.categories:
            movieCategoryVo = {"movie": page.movie, "categories": page.categories}
            self.send(movieCategoryVo, "/movie/relation/category/save")
        if page.director:
            movieDirectVo = {"movie": page.movie, "director": page.director}
            self.send(movieDirectVo, "/movie/relation/director/save")
        if page.label:
            movieLabelVo = {"movie": page.movie, "label": page.label}
            self.send(movieLabelVo, "/movie/relation/label/save")
        if page.sampleimage:
            movieSampleImageVo = {"movie": page.movie, "sampleImages": page.sampleimage}
            self.send(movieSampleImageVo, "/movie/relation/sampleimage/save")
        if page.stars:
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
        if page.studio:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series:
            movieSeriesVo = {"movie": page.movie, "studio": page.series}
            self.send(movieSeriesVo, "/movie/relation/series/save")
