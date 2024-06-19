import base64
import os
from fake_useragent import UserAgent
import requests

from utils.RequestUtil import RequestUtil
from utils.LogUtil import LogUtil
from utils.WebUtil import WebUtil
from utils.attrs.Image import Image


class ImageUtil:
    ua = None
    basePath = ""
    logUtil = LogUtil()
    requestUtil = RequestUtil()
    logFilePath = "./image.log"
    webUtil = WebUtil()

    def __init__(self) -> None:
        self.ua = UserAgent()

    def downloadSampleImages(self, links, actresses, code):
        if actresses == None or len(actresses) < 1:
            actresses = ["未知演员"]
        headers = {"User-Agent": self.ua.random}
        imageList = []
        nameList = []
        image = Image()
        for link in links:
            filename = link.split("/")[-1]
            # if self.__checkFileIsExists(
            #   actresses=actresses, code=code, filename=filename, isBigImage=False
            # ):
            # self.logUtil.log(
            #     "local sample file "
            #     + filename
            #     + " already exists skipping download",
            #     log_file_path=self.logFilePath,
            # )
            # continue
            # 下载图片
            response = requests.get(link, headers=headers, verify=False)
            self.logUtil.log(
                "image response code is " + str(response.status_code),
                log_file_path=self.logFilePath,
            )
            if response.status_code == 200:
                self.logUtil.log(
                    "image " + response.url + " download success",
                    log_file_path=self.logFilePath,
                )
                # self.__save2Local(
                #    response=response,
                #    actresses=actresses,
                #    code=code,
                #    filename=filename,
                #    isBigImage1=False,
                # )
                imageList.append(base64.b64encode(response.content).decode("utf-8"))
                nameList.append(filename)
            else:
                # 可能会有下载失败的情况
                self.logUtil.log(
                    "sampleimage " + response.url + " download failure",
                    log_file_path=self.logFilePath,
                )
        if imageList and len(imageList) >= 1:
            image.actresses = actresses
            image.code = code
            image.names = nameList
            image.images = imageList
            path = "/sampleimage/save/sample"
            self.requestUtil.sendImage(
                image.toDict(),
                path=path,
            )

    def downloadBigImage(self, link, actresses, code):
        if actresses == None or len(actresses) < 1:
            actresses = ["未知演员"]
        filename = link.split("/")[-1]
        imageList = []
        nameList = []
        image = Image()
        # if self.__checkFileIsExists(
        #    actresses=actresses, code=code, filename=filename, isBigImage=True
        # ):
        #   self.logUtil.log(
        #      "local bigImage file " + filename + " already exists skipping download",
        #     log_file_path=self.logFilePath,
        # )
        # return
        headers = {"User-Agent": self.ua.random}
        response = requests.get(link, headers=headers, verify=False)
        self.logUtil.log(
            "image response code is " + str(response.status_code),
            log_file_path=self.logFilePath,
        )
        self.logUtil.log(
            "image response url is " + response.url,
            log_file_path=self.logFilePath,
        )
        if response.status_code == 200:
            self.logUtil.log(
                "image " + response.url + " download success",
                log_file_path=self.logFilePath,
            )
            filename = link.split("/")[-1]
            # self.__save2Local(
            #    response=response,
            #    actresses=actresses,
            #    code=code,
            #    filename=filename,
            #    isBigImage=True,
            # )
            imageList.append(base64.b64encode(response.content).decode("utf-8"))
            nameList.append(filename)
        else:
            self.logUtil.log(
                "bigimage " + response.url + " download failure",
                log_file_path=self.logFilePath,
            )
        if imageList and len(imageList) >= 1:
            path = "/bigimage/save/local"
            image.actresses = actresses
            image.code = code
            image.names = nameList
            image.images = imageList
            self.requestUtil.sendImage(
                image.toDict(),
                path=path,
            )

    def __save2Local(self, response, actresses, code, filename, isBigImage):
        if not isBigImage:
            targetFolder = self.basePath + actresses + "/" + code + "/" + "sample" + "/"
        else:
            targetFolder = (
                self.basePath + actresses + "/" + code + "/" + "bigImage" + "/"
            )
        path = targetFolder + filename
        self.logUtil.log(
            "current image store path is " + path,
            log_file_path=self.logFilePath,
        )
        if self.__checkFolderIsExists(targetFolder):
            self.__save(response, path)
        else:
            self.logUtil.log(
                "create folder " + targetFolder,
                log_file_path=self.logFilePath,
            )
            os.makedirs(targetFolder)
            self.__save(response, path)
        self.logUtil.log(
            "image " + path + " is downloaded",
            log_file_path=self.logFilePath,
        )

    def __checkFolderIsExists(self, path):
        if os.path.exists(path):
            self.logUtil.log(
                path + " exists",
                log_file_path=self.logFilePath,
            )
            return True
        self.logUtil.log(
            path + " not exists",
            log_file_path=self.logFilePath,
        )
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
