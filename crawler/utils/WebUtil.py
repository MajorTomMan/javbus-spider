import time
import warnings
import requests
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc

options = ChromeOptions()
warnings.simplefilter("ignore", ResourceWarning)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-web-security")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument("--user-data-dir=/dev/null")
options.add_argument("--remote-debugging-port=12000")
options.page_load_strategy = "normal"

driver = Chrome(
    headless=False,
    driver_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
    options=options,
    version_main=122,
)


class WebUtil:

    def getWebSite(self, link):
        print("starting request to " + link + " ...........")
        print("watting for request finished...........")
        star_time = time.time()
        driver.get(link)
        end_time = time.time()
        print("request finished....")
        print("spend time was " + str(end_time - star_time))
        print("driver will be quit")
        source = driver.page_source
        driver.quit()
        return source

    def save2local(self, path, filename, content):
        with open(path + "/" + filename + ".html", "w", encoding="utf-8") as f:
            f.write(content)

    def checkisLimitedByAge(self, content):
        if "Age" in content:
            return True
        elif "Verification" in content:
            return True
        else:
            return False

    def usingSeleniumToFix(self, driver):
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
            print("checkbox not found")
