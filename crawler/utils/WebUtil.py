import time
from urllib.parse import urlparse, urlunparse
import warnings
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc

from utils.LogUtil import LogUtil

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
# options.add_argument("--remote-debugging-port=12000")
# 使用eager加快加载速度
options.page_load_strategy = "eager"


class WebUtil:
    driver = None
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

    @classmethod
    def getWebSite(cls, link):
        parsed_url = urlparse(link)
        for base_url in cls.baseUrls:
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
                if cls.driver is None:
                    cls.logUtil.log("driver initial")
                    cls.driver = Chrome(
                        headless=True,
                        driver_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
                        options=options,
                        version_main=122,
                    )
                    cls.driver.set_page_load_timeout(120)
                    cls.driver.set_script_timeout(120)

                cls.logUtil.log("starting request to " + new_url + " ...........")
                cls.logUtil.log("waiting for request finished...........")
                start_time = time.time()
                cls.driver.get(new_url)
                end_time = time.time()
                cls.logUtil.log("request finished....")
                cls.logUtil.log("request spend time was " + str(end_time - start_time))
                source = cls.driver.page_source
                return source
            except TimeoutException:
                cls.logUtil.log("request to " + new_url + " timeout in 2 minutes")
                cls.logUtil.log("waiting 5 seconds to request")
                continue
            except WebDriverException as e:
                cls.logUtil.log(e)
                continue
        cls.logUtil.log("All backup URLs tried, none successful.")
        return None

    def save2local(cls, path, filename, content):
        with open(path + "/" + filename + ".html", "w", encoding="utf-8") as f:
            f.write(content)

    def checkisLimitedByAge(cls, content):
        if "Age" in content:
            return True
        elif "Verification" in content:
            return True
        else:
            return False

    def usingSeleniumToFix(cls, driver):
        checkbox = driver.find_element(
            By.XPATH, "/html/body/div[5]/div/div/div[2]/form/div/label/input"
        )
        if checkbox:
            checkbox.click()
            submit = driver.find_element(
                By.XPATH, "/html/body/div[5]/div/div/div[2]/form/input"
            )
            if submit:
                submit.click()
        else:
            cls.logUtil.log("checkbox not found")
