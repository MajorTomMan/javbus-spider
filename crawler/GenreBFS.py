import hashlib
import os
import threading
import time
from urllib.parse import urlparse
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
    lock = threading.Lock()
    requestUtil = RequestUtil()

    def __init__(self, url, is_censored):
        if is_censored == True:
            self.genreUrl = url + "genre/"
        else:
            self.genreUrl = url + "uncensored/genre"
        self.isCensored = is_censored

    def BFS(self):
        source = None
        star_time = time.time()
        if self.genreUrl:
            while not source:
                source = self.webUtil.getWebSite(self.genreUrl)
                self.logUtil.log("retry to connecting " + self.genreUrl)
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
                    if vos and len(vos) >= 1:
                        self.requestUtil.send(vos, "/genre/relation/category/save")

            else:
                self.save2local(source, self.genreUrl, ".html")
                self.logUtil.log("boxs not found")
        else:
            self.save2local(source, self.genreUrl, ".html")
            self.logUtil.log("h4s not found")

    def printGenres(self, vos):
        with genre.lock:
            self.logUtil.log(vos)

    def save2local(self, content, link, extensions):
        # 获取链接的路径名
        parsed_url = urlparse(link)
        path_name = parsed_url.path.replace("/", "_")
        # 计算路径名的哈希值
        hash_value = hashlib.md5(path_name.encode()).hexdigest()

        # 构建保存文件的路径
        save_path = f"./failed_link/{path_name}_{hash_value}{extensions}"
        with open(save_path, "w+", encoding="UTF-8") as f:
            f.write(content)
