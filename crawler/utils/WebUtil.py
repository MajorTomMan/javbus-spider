import time
import os
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    NoSuchWindowException,
)
from utils.LogUtil import LogUtil
from urllib3.exceptions import MaxRetryError
from winproxy import ProxySetting

proxy = ProxySetting()


class WebUtil:
    _instance = None
    _lock = threading.Lock()

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
        self.local = threading.local()
        self.lock = threading.Lock()

    def initialize_driver(self, isNormal=False):
        options = ChromeOptions()
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        if isNormal:
            options.page_load_strategy = "normal"
        else:
            options.page_load_strategy = "eager"
        self.local.options = options
        self.logUtil.log("driver initial")
        self.local.driver = Chrome(
            # driver_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
            browser_executable_path="C:\\Users\\master\\Desktop\\Soft\\Chrome\\chrome.exe",
            options=self.local.options,
            version_main=125,
            use_subprocess=True,
        )
        self.local.driver.set_page_load_timeout(3600)
        self.local.driver.set_script_timeout(3600)

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
            except TimeoutException as e:
                self.logUtil.log("request timeout reason:" + e.msg)
                self.logUtil.log("request to " + new_url + " timeout in 2.5 minutes")
                self.logUtil.log("waiting 5 seconds to request backup link")
                time.sleep(5)
                if self.local.driver:
                    self.local.driver.quit()
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
            except ConnectionResetError:
                self.logUtil.log("Connection reset skipping")
            except NoSuchElementException:
                self.logUtil.log("torrent not found origin:" + new_url + " skipping")
            except NoSuchWindowException as e:
                self.logUtil.log(e.msg)
        self.logUtil.log("All backup URLs tried, none successful.")
        return None

    def send(self, new_url, isNormal):
        self.initialize_driver(isNormal)
        self.logUtil.log(
            "starting request to " + new_url + " ...........",
            log_file_path=self.logFilePath,
        )
        self.logUtil.log("waiting for request finished...........")
        start_time = time.time()
        if isNormal:
            self.local.driver.implicitly_wait(500)
        self.local.driver.get(new_url)
        end_time = time.time()
        self.logUtil.log("request finished....", log_file_path=self.logFilePath)
        self.logUtil.log("request spend time was " + str(end_time - start_time))
        source = self.local.driver.page_source
        self.local.driver.quit()
        return source

    def checkIsBeDetected(self, source):
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title:
            if "Age" in bs.title.text:
                return True
        return False

    def cleanChromeDriver(self):
        try:
            os.system("taskkill /F /im chromedriver.exe")
            os.system("taskkill /F /im undetected_chromedriver.exe")
            os.system("taskkill /F /im chrome.exe")
        except TypeError:
            pass
