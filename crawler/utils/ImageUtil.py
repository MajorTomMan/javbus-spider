import os
from fake_useragent import UserAgent
import requests

from utils.LogUtil import LogUtil


class ImageUtil:
    ua = None
    basePath = ""
    logUtil = LogUtil()

    def __init__(self) -> None:
        self.ua = UserAgent()
        self.basePath = "./images/"

    def downloadSampleImages(self, links, actresses, code):
        if actresses == None or len(actresses) < 1:
            actresses = "未知演员"
        elif len(actresses) > 1:
            actresses = "-".join(actresses)
        elif len(actresses) == 1:
            actresses = actresses[0]
        headers = {"User-Agent": self.ua.random}
        for link in links:
            filename = link.split("/")[-1]
            if self.__checkFileIsExists(
                actresses=actresses, code=code, filename=filename, isBigImage=False
            ):
                self.logUtil.log(
                    "local sample file "
                    + filename
                    + " already exists skipping download"
                )
                continue
            response = requests.get(link, headers=headers)
            self.logUtil.log("image response code is " + str(response.status_code))
            if response.status_code == 200:
                self.logUtil.log("image " + response.url + " download success")
                self.__save2Local(
                    response=response,
                    actresses=actresses,
                    code=code,
                    filename=filename,
                    isBigImage=False,
                )
            else:
                self.logUtil.log("image " + response.url + " download failure")

    def downloadBigImage(self, link, actresses, code):
        if actresses == None or len(actresses) < 1:
            actresses = "未知演员"
        elif len(actresses) > 1:
            actresses = "-".join(actresses)
        elif len(actresses) == 1:
            actresses = actresses[0]
        filename = link.split("/")[-1]
        if self.__checkFileIsExists(
            actresses=actresses, code=code, filename=filename, isBigImage=True
        ):
            self.logUtil.log(
                "local bigImage file " + filename + " already exists skipping download"
            )
            return
        headers = {"User-Agent": self.ua.random}
        response = requests.get(link, headers=headers)
        self.logUtil.log("image response code is " + str(response.status_code))
        self.logUtil.log("image response url is " + response.url)
        if response.status_code == 200:
            self.logUtil.log("image " + response.url + " download success")
            url = response.url
            paths = url.split("/")
            filename = paths[-1]
            self.__save2Local(
                response=response,
                actresses=actresses,
                code=code,
                filename=filename,
                isBigImage=True,
            )
        else:
            self.logUtil.log("image " + response.url + " download failure")

    def __save2Local(self, response, actresses, code, filename, isBigImage):
        if not isBigImage:
            targetFolder = self.basePath + actresses + "/" + code + "/" + "sample" + "/"
        else:
            targetFolder = (
                self.basePath + actresses + "/" + code + "/" + "bigImage" + "/"
            )
        path = targetFolder + filename
        self.logUtil.log("current image store path is " + path)
        if self.__checkFolderIsExists(targetFolder):
            self.__save(response, path)
        else:
            self.logUtil.log("create folder " + targetFolder)
            os.makedirs(targetFolder)
            self.__save(response, path)
        self.logUtil.log("image " + path + " is downloaded")

    def __checkFolderIsExists(self, path):
        if os.path.exists(path):
            self.logUtil.log(path + " exists")
            return True
        self.logUtil.log(path + " not exists")
        return False

    def __checkFileIsExists(self, actresses, code, filename, isBigImage):
        if not isBigImage:
            path = (
                self.basePath + actresses + "/" + code + "/" + "sample" + "/" + filename
            )
        else:
            path = (
                self.basePath
                + actresses
                + "/"
                + code
                + "/"
                + "bigImage"
                + "/"
                + filename
            )
        if os.path.exists(path):
            return True
        return False

    def __save(self, response, path):
        with open(path, "wb") as f:
            for cache in response.iter_content(chunk_size=32):
                f.write(cache)
