from utils.Utils import WebUtil,AttrsUtil,ImageUtil

from bs4 import BeautifulSoup


class search:
    def __init__(self,url,name) -> None:
        self.imageUtil=ImageUtil()
        self.attrsUtil=AttrsUtil()
        self.webUtil=WebUtil()
        self.searchUrl=url+"/search/"+name
    # 默认是搜索模式
    def bfs(self):
        if self.searchUrl:
            driver=self.webUtil.getWebSite(self.searchUrl)
            if self.webUtil.checkisLimitedByAge(driver.title):
                return
    def __bfs(self,driver):
        bs=BeautifulSoup(driver.page_source,"html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.attrsUtil.getLink(brick)
                print("now visit website link is "+link)
                if link:
                    self.links.append(link)
                    self.__parseDetailPage(link)
                break
            print("all link was visited jump to next page")
        else:
            print("movie list not found")