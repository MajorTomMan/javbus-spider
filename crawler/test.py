from bs4 import BeautifulSoup
from utils.ActressUtil import ActressUtil
from utils.AttrsUtil import AttrsUtil
from utils.LogUtil import LogUtil
from utils.PageUtil import PageUtil
from utils.RequestUtil import RequestUtil
from utils.WebUtil import WebUtil

webUtil = WebUtil()
actressUtil = ActressUtil()
attrsUtil = AttrsUtil()
logUtil = LogUtil()
requestUtil = RequestUtil()
pageUtil = PageUtil("https://www.cdnbus.shop/", False)


bs = BeautifulSoup(
    webUtil.getWebSite("https://www.cdnbus.shop/072823-001"), "html.parser"
)
LogUtil().log(pageUtil.getPage(bs))
