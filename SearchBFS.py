from bs4 import BeautifulSoup
from utils.Utils import WebUtil,AttrsUtil,ImageUtil,PageUtil



class search:
    WebUtil=WebUtil()
    PageUtil
    AttrsUtil=AttrsUtil()
    links=[]
    attrsList=[]
    searchUrl=""
    pageNum=1
    def __init__(self,url,name) -> None:
        self.searchUrl=url+"/search/"+name+"/"
        self.PageUtil=PageUtil(url)
    # 默认是搜索模式
    def BFS(self):
        while(self.pageNum<2):
            if self.searchUrl:
                driver=self.WebUtil.getWebSite(self.searchUrl+str(self.pageNum))
                if self.WebUtil.checkisLimitedByAge(driver.title):
                    return
                self.__bfs(driver)
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