import time
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.RequestUtil import RequestUtil
from utils.AttrsUtil import AttrsUtil


from utils.attrs.Category import Category

from utils.WebUtil import WebUtil


class genre:
    webUtil = WebUtil()
    attrsUtil = AttrsUtil()
    request = RequestUtil()
    logUtil = LogUtil()
    genreUrl = ""
    isCensored = True

    def __init__(self, url, is_censored):
        if is_censored == True:
            self.genreUrl = url + "genre/"
        else:
            self.genreUrl = url + "uncensored/genre"
        self.isCensored = is_censored

    def BFS(self):
        star_time = time.time()
        if self.genreUrl:
            source = self.webUtil.getWebSite(self.genreUrl)
            if source:
                self.__bfs(source)
            self.logUtil.log("bfs done")
        end_time = time.time()
        self.logUtil.log("thread running time is " + str(end_time - star_time))

    def __bfs(self, source):
        if not source:
            return
        genres = []
        bs = BeautifulSoup(source, "html.parser")
        titles = bs.find_all("h4", {"class": "modal-title"})
        for title in titles:
            bs.find("h4", {"class": "modal-title"}).extract()
        h4s = bs.find_all("h4")
        for h4 in h4s:
            genres.append(h4.text.strip())
        if h4s:
            boxs = bs.find_all("div", {"class": "row genre-box"})
            if boxs:
                vos = []
                for index, box in enumerate(boxs):
                    cs = self.attrsUtil.getCategories(box)
                    categories = []
                    for k, v in cs.items():
                        category = Category()
                        category.name = k
                        category.link = v
                        category.is_censored = self.isCensored
                        categories.append(category.toDict())
                    key = genres[index]
                    vos = {
                        "genre": {"name": key},
                        "categories": categories,
                    }
                    self.logUtil.log(vos)
                    if vos and len(vos) >= 1:
                        response = self.request.post(
                            vos, "/genre/relation/category/save"
                        )
                        if response:
                            if response.status_code == 200:
                                self.logUtil.log(
                                    "send data to /genre/relation/category/save was success "
                                )
                            else:
                                self.logUtil.log(
                                    "send data to /genre/relation/category/save was failure "
                                )
                        else:
                            self.logUtil.log(
                                "request not response pls check server is open or has expection "
                            )
            else:
                self.logUtil.log("boxs not found")
        else:
            self.logUtil.log("h4s not found")
