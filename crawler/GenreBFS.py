from bs4 import BeautifulSoup
from utils.RequestUtil import RequestUtil
from utils.AttrsUtil import AttrsUtil


from utils.attrs.Category import Category

from utils.WebUtil import WebUtil


class GenreBFS:
    genreUrl = ""
    webUtil = WebUtil()
    attrsUtil = AttrsUtil()
    request = RequestUtil()

    def __init__(self, url) -> None:
        self.genreUrl = url + "genre/"

    def BFS(self):
        if self.genreUrl:
            source = self.webUtil.getWebSite(self.genreUrl)
            self.__bfs(source)
            print("bfs done")

    def __bfs(self, source):
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
                        categories.append(category.toDict())
                    key = genres[index]
                    vos = {
                        "genre": {"name": key},
                        "categories": categories,
                        "is_censored": True,
                    }
                    if vos and len(vos) >= 1:
                        self.request.post(vos, "/genre/relation/category/save")
            else:
                print("boxs not found")
        else:
            print("h4s not found")
