import time
import os
from urllib.parse import urlparse, urlunparse
import threading
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage
from utils.LogUtil import LogUtil
from winproxy import ProxySetting

proxy = ProxySetting()


class WebUtil:
    _instance = None
    _lock = threading.Lock()
    page = None
    options = None
    logUtil = LogUtil()
    baseUrls = [
        "https://www.seedmm.shop/",
        "https://www.seejav.shop/",
        "https://www.cdnbus.shop/",
        "https://www.buscdn.shop/",
        "https://www.dmmsee.art",
        "https://www.busfan.shop",
        "https://www.busfan.art",
        "https://www.busdmm.shop",
        "https://www.javsee.art/",
        "https://www.javsee.shop",
        "https://www.cdnbus.art",
        "https://www.buscdn.art",
    ]
    logFilePath = "./driver.log"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(WebUtil, cls).__new__(cls)
                    cls._instance.__init_once()
        return cls._instance

    def __init_once(self):
        self.lock = threading.Lock()
        self.page = self.initialize_driver()

    def initialize_driver(self):
        options = ChromiumOptions()
        options.auto_port()
        options.ignore_certificate_errors()
        options.no_imgs(True).mute(True)
        options.headless()
        options.set_argument("--no-sandbox")  # 无沙盒模式
        return ChromiumPage(options)

    def getWebSite(self, link, isNormal=False):
        parsed_url = urlparse(link)
        for base_url in self.baseUrls:
            base_parsed_url = urlparse(base_url)
            new_url = urlunparse(
                (
                    base_parsed_url.scheme,
                    base_parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    parsed_url.query,
                    parsed_url.fragment,
                )
            )
            try:
                source = self.send(new_url, isNormal)
                if self.checkIsBeDetected(source):
                    return None
                return source
            except Exception as e:
                self.logUtil.log(e)
        self.logUtil.log("All backup URLs tried, none successful.")
        return None

    def send(self, new_url, isNormal):
        self.logUtil.log(
            "starting request to " + new_url + " ...........",
            log_file_path=self.logFilePath,
        )
        self.logUtil.log("waiting for request finished...........")
        start_time = time.time()
        tag = self.page.new_tab()
        tag.get(new_url)
        end_time = time.time()
        source = tag.html
        self.logUtil.log("request finished....", log_file_path=self.logFilePath)
        self.logUtil.log("request spend time was " + str(end_time - start_time))
        tag.close()
        return source

    def checkIsBeDetected(self, source):
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title:
            if "Age" in bs.title.text:
                return True
        return False

    def close(self):
        self.page.quit()
