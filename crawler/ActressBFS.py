import hashlib
import json
import threading
import time
from urllib.parse import urlparse
from warnings import catch_warnings
from bs4 import BeautifulSoup
from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil

from utils.AttrsUtil import AttrsUtil
from utils.ActressUtil import ActressUtil
from utils.WebUtil import WebUtil
from utils.exceptions.PageException import PageException


class actresses:
    webUtil = WebUtil()
    actressUtil = ActressUtil()
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()
    requestUtil = RequestUtil()
    vos = []
    starUrl = ""
    pageNum = 1
    baseUrl = ""
    timeouts = []
    isCensored = True
    lock = threading.Lock()
    pageUtil = None

    def __init__(self, url, is_censored):
        self.baseUrl = url
        self.isCensored = is_censored
        self.pageUtil = PageUtil(url, is_censored)

    def BFS(self):
        star_time = time.time()
        while True:
            if self.isCensored:
                link = self.baseUrl + "actresses/" + str(self.pageNum)
            else:
                link = self.baseUrl + "uncensored/actresses/" + str(self.pageNum)
            source = self.webUtil.getWebSite(link)
            self.logUtil.log("now page num is " + str(self.pageNum))
            bs = BeautifulSoup(source, "html.parser")
            if self.pageUtil.hasNextPage(bs):
                try:
                    self.__bfs(source)
                except PageException:
                    self.save2local(source, link, ".html")
            else:
                self.logUtil.log("final page is reach")
                try:
                    self.__bfs(source)
                except PageException:
                    self.save2local(source, link, ".html")
                break
            self.pageNum += 1
        end_time = time.time()
        self.logUtil.log("bfs done")
        self.logUtil.log("thread running time is " + str(end_time - star_time))

    def __bfs(self, source):
        if not source:
            return
        actressList = []
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                actress_dict = self.attrsUtil.getSingleActressLink(brick)
                if actress_dict:
                    try:
                        actress = self.actressUtil.getActressDetails(
                            actress_dict["actress_link"]
                        )
                    except Exception as e:
                        self.save2local(
                            source,
                            threading.currentThread().getName() + "__bfs",
                            ".html",
                        )
                    if actress:
                        if not self.actressUtil.matchLinkIsCompanyLink(
                            actress_dict["photo_link"]
                        ):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                actress.photo_link = url + actress.photo_link
                        actress.actress_link = actress_dict["actress_link"]
                        actress.is_censored = self.isCensored
                        actressList.append(actress.toDict())
                    else:
                        self.timeouts.append(
                            {
                                "name": actress_dict["name"],
                                "link": actress_dict["actress_link"],
                            }
                        )
                        self.logUtil.log(
                            "request "
                            + actress_dict["name"]
                            + ":"
                            + actress_dict["actress_link"]
                            + " timeout  add it to timeouts"
                        )
                    self.send(actressList, "/actress/save")
                else:
                    self.save2local(
                        source, threading.currentThread().getName() + "__bfs", ".html"
                    )
            if self.timeouts and len(self.timeouts) >= 1:
                self.logUtil.log("try to request timeout list")
                for timeout in self.timeouts:
                    actress = self.actressUtil.getActressDetails(link=timeout["link"])
                    if actress:
                        if self.actressUtil.matchLinkIsCompanyLink(
                            actress_dict["photo_link"]
                        ):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                actress.photo_link = url + actress.photo_link
                            else:
                                actress.photo_link = self.baseUrl + actress.photo_link
                        actress.actress_link = timeout["link"]
                        self.send(
                            {"actress": actressList},
                            "/actress/save",
                        )
                        self.logUtil.log(
                            "retry "
                            + timeout["name"]
                            + timeout["link"]
                            + " was success"
                        )
                    else:
                        self.logUtil.log(
                            "retry "
                            + timeout["name"]
                            + timeout["link"]
                            + " was failure name abandon"
                        )
        else:
            self.save2local(
                source, threading.currentThread().getName() + "__bfs", ".html"
            )
            self.logUtil.log("bricks not found")
            raise PageException()

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

    def printActresses(self, actress):
        with actresses.lock:
            self.logUtil.log("info of " + actress.name + " was collected")
            self.logUtil.log(
                "----------------actress info start-----------------------------"
            )
            self.logUtil.log(actress)
            self.logUtil.log(
                "----------------actress info over-----------------------------"
            )
