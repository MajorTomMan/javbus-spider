import json
import orjson
from bs4 import BeautifulSoup
from utils.Utils import AttrsUtil, PageUtil, WebUtil,RequestUtil

class index:
    WebUtil=WebUtil()
    PageUtil
    AttrsUtil=AttrsUtil()
    RequestUtil=RequestUtil()
    links=[]
    pageNum = 1
    baseUrl=""
    def __init__(self,url):
        self.baseUrl = url+"page/"+str(self.pageNum)
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
                    page=self.PageUtil.parseDetailPage(link)
                    if page:
                        print("------------------------------page info start--------------------------------------")
                        print(page)
                        print("------------------------------page info ended--------------------------------------")
                        if page.stars:
                            print("------------------------------star info start--------------------------------------")
                            for star in page.stars:
                                print("star: "+str(star))
                            print("------------------------------star info ended--------------------------------------")
                        self.sendData2Server(page.stars,"/star/save")
                        self.sendData2Server(page.categories,"/category/save")
                        self.sendData2Server(page.studio,"/studio/save")
                        self.sendData2Server(page.series,"/series/save")
                        self.sendData2Server(page.label,"/label/save")
                        self.sendData2Server(page.director,"/director/save")
                        self.sendData2Server(page.movie,"/movie/save")
                        self.sendData2Server(page)
                    
            print("all link was visited jump to next page")
        else:
            print("page list not found")
    def save2local(self,content):
        with open("./headers/requests.txt") as f:
            f.write(content)
    def sendData2Server(self,data,path):
        response=self.RequestUtil.post(data=data,path=path)
        if response.status_code==200:
            print("send data was success")
        else:
            print("send data was failure")