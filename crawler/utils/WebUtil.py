import time
from urllib.parse import urlparse, urlunparse
import threading
import warnings
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from browsermobproxy import Server
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
    server=None
    proxy=None
    def __init__(self) -> None:
        self.local = threading.local()
        self.server=Server("proxy\\bin\\browsermob-proxy.bat")
        self.server.start()
        self.proxy=self.server.create_proxy()

    def initialize_driver(self, isNormal=False):
        options = ChromeOptions()
        warnings.simplefilter("ignore", ResourceWarning)
        options.add_argument("--disable-images")
        options.add_argument("--disable-gpu")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--proxy-server={0}".format(self.proxy.proxy))
        # 使用eager加快加载速度
        options.page_load_strategy = "eager"
        # options.add_argument("--remote-debugging-port=12000")
        self.local.options = options
        self.logUtil.log("driver initial")
        self.local.driver = Chrome(
            headless=False,
            #driver_executable_path="C:\\Users\\master\\Desktop\\Soft\\Chrome\\chromedriver.exe",
            #browser_executable_path="C:\\Users\\master\\Desktop\\Soft\\Chrome\\Chrome.exe",
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
        self.proxy.new_har("https://www.cdnbus.shop/ajax/uncledatoolsbyajax.php",options={'captureContent': True})
        self.local.driver.get(new_url)
        self.proxy.wait_for_traffic_to_stop(1,240)
        end_time = time.time()
        self.logUtil.log("request finished....", log_file_path=self.logFilePath)
        self.logUtil.log(
            "request spend time was " + str(end_time - start_time),
        )
        har=self.proxy.har
        for entry in har["log"]["entries"]:
            if "uncledatoolsbyajax.php" in entry["request"]["url"]:
                if entry["response"]["status"] == 200:
                    source=BeautifulSoup(self.local.driver.page_source,"html.parser")
                    table=source.find("table",id="magnet-table")
                    tag=source.new_tag("p")
                    tag.string=str(entry["response"]["content"]["text"])
                    if table:
                        table.append(tag)
                    self.local.driver.quit()
                    return str(source)
        source = self.local.driver.page_source
        self.local.driver.quit()

        return source

    def checkIsBeDetected(self, source):
        bs = BeautifulSoup(source, "html.parser")
        if bs and bs.title:
            if "Age" in bs.title.text:
                return True
            return False
