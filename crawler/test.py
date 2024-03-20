from bs4 import BeautifulSoup
from utils.ActressUtil import ActressUtil
from utils.AttrsUtil import AttrsUtil
from utils.LogUtil import LogUtil
from utils.MailUtil import MailUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.WebUtil import WebUtil
import undetected_chromedriver as uc


if __name__ == "__main__":
    # driver = uc.Chrome()
    # driver.get("https://www.baidu.com")
    # driver.quit()
    MailUtil().send_email("hello from spider")
