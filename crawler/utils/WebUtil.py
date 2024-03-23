import time
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException

from utils.LogUtil import LogUtil
from urllib3.exceptions import MaxRetryError


class WebUtil:
    options = None
    logUtil = LogUtil()
    baseUrls = [
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

    def __init__(self) -> None:
        self.local = threading.local()

    def initialize_driver(self):
        options = ChromeOptions()
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        # 使用eager加快加载速度
        options.page_load_strategy = "eager"
        # options.add_argument("--remote-debugging-port=12000")
        self.local.options = options
        self.logUtil.log("driver initial")
        self.local.driver = Chrome(
            headless=True,
            driver_executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe",
            options=self.local.options,
            version_main=122,
            user_multi_procs=True,
            use_subprocess=True,
        )
        # 超时时间设为2.5分钟
        self.local.driver.set_page_load_timeout(150)
        self.local.driver.set_script_timeout(150)

    def getWebSite(self, link):
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
                source = self.send(new_url)
                if self.checkIsBeDetected(source):
                    return None
                return source
            except TimeoutException:
                self.logUtil.log(
                    "request to " + new_url + " timeout in 2.5 minutes",
                )
                self.logUtil.log(
                    "waiting 5 seconds to request backup link",
                )
                time.sleep(5)
                continue
            except WebDriverException as e:
                self.logUtil.log(e)
                self.local.driver.quit()
                continue
            except MaxRetryError as e:
                self.logUtil.log("MaxRetry Link->")
                self.logUtil.log(e.reason)
                continue
        self.logUtil.log("All backup URLs tried, none successful.")
        return None

    def send(self, new_url):
        self.initialize_driver()
        self.logUtil.log(
            "starting request to " + new_url + " ...........",
            log_file_path=self.logFilePath,
        )
        self.logUtil.log(
            "waiting for request finished...........",
        )
        start_time = time.time()
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
