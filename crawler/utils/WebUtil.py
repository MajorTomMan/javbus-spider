import time
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException

from utils.LogUtil import LogUtil
from urllib3.exceptions import MaxRetryError
from winproxy import ProxySetting

proxy = ProxySetting()


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
    lock = threading.Lock()

    def __init__(self) -> None:
        self.local = threading.local()

    def initialize_driver(self, isNormal=False):
        options = ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs", {"performance": "INFO", "browser": "INFO"}
        )
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        # 使用eager加快加载速度
        if not isNormal:
            options.page_load_strategy = "eager"
        else:
            options.page_load_strategy = "normal"
        # options.add_argument("--remote-debugging-port=12000")
        self.local.options = options
        self.logUtil.log("driver initial")
        self.local.driver = Chrome(
            headless=False,
            driver_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
            options=self.local.options,
            version_main=123,
            user_multi_procs=True,
            use_subprocess=True,
        )
        self.local.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": open("utils\hook.js", encoding="utf-8").read()},
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
            except ConnectionResetError as e:
                self.logUtil.log("Connection reset skipping")
        self.logUtil.log("All backup URLs tried, none successful.")
        return None

    def send(self, new_url, isNormal):
        self.initialize_driver(False)
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
        entity = self.local.driver.get_log("browser")

        """
         torrent=""
        for e in entity:
            if e["level"] == "INFO" and "tr" in e["message"]:
                self.logUtil.log(
                    "console.log->" + e["message"],
                ) 
        """
        source = self.local.driver.page_source
        self.local.driver.quit()

        return source

    def checkIsBeDetected(self, source):
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title:
            if "Age" in bs.title.text:
                return True
            return False
