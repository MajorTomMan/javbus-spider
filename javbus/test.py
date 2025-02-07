from bs4 import BeautifulSoup
from utils.ActressUtil import ActressUtil
from utils.AttrsUtil import AttrsUtil
from utils.LogUtil import LogUtil
from utils.MailUtil import MailUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.WebUtil import WebUtil
from DrissionPage import ChromiumPage, SessionPage, ChromiumOptions
from Index import index
import requests


if __name__ == "__main__":
    # response=requests.get("https://pics.dmm.co.jp/mono/movie/adult/ofje377/ofje377pl.jpg")
    # print(response.status_code)
    page=WebUtil().getWebSite(
        "https://www.javlibrary.com/cn/vl_searchbyid.php?keyword=pmv"
    )
    print(page.html)

    # driver = uc.Chrome()
    # driver.get("https://www.baidu.com")
    # driver.quit()
    # MailUtil().send_email("hello from spider")
    # index("https://www.cdnbus.shop/",True).DFS("https://www.cdnbus.shop/WAAA-363")
    # index("https://www.cdnbus.shop/",True).BFS()
