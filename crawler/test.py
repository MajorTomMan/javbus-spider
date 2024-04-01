'''
Date: 2024-03-31 18:33:06
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2024-03-31 22:24:43
FilePath: \crawler\test.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''
from bs4 import BeautifulSoup
from utils.ActressUtil import ActressUtil
from utils.AttrsUtil import AttrsUtil
from utils.LogUtil import LogUtil
from utils.MailUtil import MailUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.WebUtil import WebUtil
import undetected_chromedriver as uc

from Index import index

if __name__ == "__main__":
    #driver = uc.Chrome()
    #driver.get("https://www.baidu.com")
    #driver.quit()
    #MailUtil().send_email("hello from spider")
    #index("https://www.cdnbus.shop/",True).DFS("https://www.cdnbus.shop/WAAA-363")
    index("https://www.cdnbus.shop/",True).BFS()