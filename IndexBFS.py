from bs4 import BeautifulSoup
from utils.Utils import AttrsUtil, PageUtil, WebUtil


class index:
    WebUtil=WebUtil()
    PageUtil
    AttrsUtil=AttrsUtil()
    links=[]
    attrsList=[]
    pageNum = 1
    baseUrl=""
    def __init__(self,url):
        self.baseUrl = url+"/page/"+str(self.pageNum)
        self.PageUtil=PageUtil(url)
    def BFS(self):
        if self.baseUrl:
            while(self.pageNum<5):
                driver=self.WebUtil.getWebSite(self.baseUrl)
                print("现在正在第"+str(self.pageNum)+"页")
                if self.WebUtil.checkisLimitedByAge(driver.title):
                    return
                self.__bfs(driver)
                break
            print("bfs done")
    def __bfs(self,driver):
        bs=BeautifulSoup(driver.page_source,"html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.AttrsUtil.getLink(brick)
                print("now visit website link is "+link)
                if link:
                    self.links.append(link)
                    attrs=self.PageUtil.parseDetailPage(link)
                    self.attrsList.append(attrs)
            print("all link was visited jump to next page")
        else:
            print("movie list not found")