import time
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc

from utils.LogUtil import LogUtil


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

    def __init__(self) -> None:
        self.local = threading.local()

    def initialize_driver(self):
        options = ChromeOptions()
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-images")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-web-security")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.page_load_strategy = "eager"
        # options.add_argument("--remote-debugging-port=12000")
        # 使用eager加快加载速度
        self.options = options
        self.logUtil.log("driver initial")
        self.driver = Chrome(
            headless=True,
            driver_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
            options=self.options,
            version_main=122,
        )
        # 超时时间设为5分钟
        self.driver.set_page_load_timeout(150)
        self.driver.set_script_timeout(150)

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
                self.initialize_driver()
                self.logUtil.log("starting request to " + new_url + " ...........")
                self.logUtil.log("waiting for request finished...........")
                start_time = time.time()
                self.driver.get(new_url)
                end_time = time.time()
                self.logUtil.log("request finished....")
                self.logUtil.log("request spend time was " + str(end_time - start_time))
                source = self.driver.page_source
                self.driver.quit()
                return source
            except TimeoutException:
                self.logUtil.log("request to " + new_url + " timeout in 2.5 minutes")
                self.logUtil.log("waiting 5 seconds to request backup")
                time.sleep(5)
                continue
            except WebDriverException as e:
                self.logUtil.log(e)
                continue
        self.logUtil.log("All backup URLs tried, none successful.")
        return None
