import base64
import os
from fake_useragent import UserAgent
import requests

from javbus.utils.request_util import RequestUtil
from javbus.utils.log_util import LogUtil
from javbus.utils.web_util import WebUtil
from javbus.items import ImageItem


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
        if not actresses:
            actresses = ["未知演员"]
        headers = {"User-Agent": self.ua.random}
        imageList = []
        nameList = []
        image = ImageItem()
        
        for link in links:
            filename = link.split("/")[-1]
            # 如果图片已经存在，跳过
            # if self.__checkFileIsExists(actresses, code, filename, isBigImage=False):
            #     self.logUtil.log(f"Local sample file {filename} already exists, skipping download.", log_file_path=self.logFilePath)
            #     continue

            try:
                response = requests.get(link, headers=headers, verify=False)
                self._log_image_response(response)

                if response.status_code == 200:
                    imageList.append(base64.b64encode(response.content).decode("utf-8"))
                    nameList.append(filename)
                else:
                    self.logUtil.log(f"Sample image {response.url} download failure.", log_file_path=self.logFilePath)
            except Exception as e:
                self.logUtil.log(f"Error downloading image from {link}: {e}", log_file_path=self.logFilePath)

        if imageList:
            image['actresses'] = actresses
            image['code'] = code
            image['names'] = nameList
            image['images'] = imageList
            path = "/sampleimage/save/sample"
            self.requestUtil.sendImage(image.toDict(), path=path)

    def downloadBigImage(self, link, actresses, code):
        if not actresses:
            actresses = ["未知演员"]
        filename = link.split("/")[-1]
        imageList = []
        nameList = []
        image = ImageItem()

        try:
            response = requests.get(link, headers={"User-Agent": self.ua.random}, verify=False)
            self._log_image_response(response)

            if response.status_code == 200:
                imageList.append(base64.b64encode(response.content).decode("utf-8"))
                nameList.append(filename)
            else:
                self.logUtil.log(f"Big image {response.url} download failure.", log_file_path=self.logFilePath)

        except Exception as e:
            self.logUtil.log(f"Error downloading big image from {link}: {e}", log_file_path=self.logFilePath)

        if imageList:
            path = "/bigimage/save/local"
            image['actresses'] = actresses
            image['code'] = code
            image['names'] = nameList
            image['images'] = imageList
            self.requestUtil.sendImage(image.toDict(), path=path)

    def _log_image_response(self, response):
        self.logUtil.log(f"Image response code: {response.status_code}", log_file_path=self.logFilePath)
        if response.status_code == 200:
            self.logUtil.log(f"Image {response.url} download success.", log_file_path=self.logFilePath)

    def __checkFolderAndFileExistence(self, path, create=False):
        """ Check if folder exists, and optionally create it. """
        if os.path.exists(path):
            self.logUtil.log(f"{path} exists.", log_file_path=self.logFilePath)
            return True
        if create:
            self.logUtil.log(f"{path} does not exist, creating folder.", log_file_path=self.logFilePath)
            os.makedirs(path)
            return True
        return False

    def __save(self, response, path):
        try:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=32):
                    f.write(chunk)
            self.logUtil.log(f"Image saved to {path}.", log_file_path=self.logFilePath)
        except Exception as e:
            self.logUtil.log(f"Error saving image to {path}: {e}", log_file_path=self.logFilePath)

    def __checkFileIsExists(self, actresses, code, filename, isBigImage):
        folder = "bigImage" if isBigImage else "sample"
        path = os.path.join(self.basePath, actresses, code, folder, filename)
        return os.path.exists(path)
