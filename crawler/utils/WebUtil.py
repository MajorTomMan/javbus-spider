import time
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
from utils.LogUtil import LogUtil
from urllib3.exceptions import MaxRetryError
from winproxy import ProxySetting

proxy = ProxySetting()


class WebUtil:
    options = None
    logUtil = LogUtil()
    baseUrls = [
        "https://www.buscdn.shop/",
        "https://www.seedmm.shop/",
        "https://www.seejav.shop/",
        "https://www.cdnbus.shop/",
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
    lock = threading.Lock()

    def __init__(self) -> None:
        self.local = threading.local()

    def initialize_driver(self, isNormal=False):
        options = ChromeOptions()
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        # 使用eager加快加载速度
        if isNormal:
            options.page_load_strategy = "normal"
        else:
            options.page_load_strategy = "eager"
        # options.add_argument("--remote-debugging-port=12000")
        self.local.options = options
        self.logUtil.log("driver initial")
        self.local.driver = Chrome(
            headless=False,
            # driver_executable_path="C:\\Users\\master\\Desktop\\Soft\\Chrome\\chromedriver.exe",
            # browser_executable_path="C:\\Users\\master\\Desktop\\Soft\\Chrome\\Chrome.exe",
            options=self.local.options,
            user_multi_procs=True,
            use_subprocess=True,
            version_main=125,
        )
        # 超时时间设为2.5分钟
        self.local.driver.set_page_load_timeout(150)
        self.local.driver.set_script_timeout(150)

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
                with self.lock:
                    proxy.registry_read()
                    if proxy.enable == True:
                        proxy.enable = False
                        proxy.registry_write()
                source = self.send(new_url, isNormal)
                if self.checkIsBeDetected(source):
                    return None
                return source
            except TimeoutException as e:
                self.logUtil.log(
                    "request timeout reason:" + e.msg,
                )
                self.logUtil.log(
                    "request to " + new_url + " timeout in 2.5 minutes",
                )
                self.logUtil.log(
                    "waiting 5 seconds to request backup link",
                )
                self.local.driver.close()
                time.sleep(5)
                continue
            except WebDriverException as e:
                self.logUtil.log(e)
                if self.local.driver:
                    self.local.driver.quit()
                continue
            except MaxRetryError as e:
                self.logUtil.log("MaxRetry Link->")
                self.logUtil.log(e.reason)
                continue
            except ConnectionResetError as e:
                self.logUtil.log("Connection reset skipping")
            except NoSuchElementException as e:
                self.logUtil.log("torrent not found origin:" + new_url + " skipping")
        self.logUtil.log("All backup URLs tried, none successful.")
        return None

    def send(self, new_url, isNormal):
        self.initialize_driver(isNormal)
        self.logUtil.log(
            "starting request to " + new_url + " ...........",
            log_file_path=self.logFilePath,
        )
        self.logUtil.log(
            "waiting for request finished...........",
        )
        start_time = time.time()
        if isNormal:
            self.local.driver.implicitly_wait(120)
        time.sleep(20)
        self.local.driver.get(new_url)
        end_time = time.time()
        self.logUtil.log("request finished....", log_file_path=self.logFilePath)
        self.logUtil.log(
            "request spend time was " + str(end_time - start_time),
        )
        source = self.local.driver.page_source
        self.local.driver.quit()
        return source

    def checkIsBeDetected(self, source):
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title:
            if "Age" in bs.title.text:
                return True
            return False
