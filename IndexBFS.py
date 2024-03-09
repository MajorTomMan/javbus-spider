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
                if link:
                    print("now visit website link is "+link)
                    self.links.append(link)
                    page=self.PageUtil.parseDetailPage(link)
                    self.save2local(vars(page),"./page/data")
                    if page:
                        print("------------------------------page info start--------------------------------------")
                        print(page)
                        print("------------------------------page info ended--------------------------------------")
                        if page.stars:
                            print("------------------------------star info start--------------------------------------")
                            for star in page.stars:
                                print("star: "+str(star))
                            print("------------------------------star info ended--------------------------------------")
                        self.sendData2Server(page.movie,"/movie/save")
                        movieBigImageVo={
                            "code":page.movie["code"],
                            "bigImage":page.bigimage,
                        }
                        movieCategoryVo={
                            "code":page.movie["code"],
                            "categories":page.categories
                        }
                        movieDirectVo={
                            "code":page.movie["code"],
                            "director":page.director
                        }
                        movieLabelVo={
                            "code":page.movie["code"],
                            "label":page.label
                        }
                        movieSampleImageVo={
                            "code":page.movie["code"],
                            "sampleImages": page.sampleimage
                        }
                        movieStarVo={
                            "code":page.movie["code"],
                            "stars":page.stars
                        }
                        movieStudioVo={
                            "code":page.movie["code"],
                            "studio":page.studio
                        }
                        movieSeriesVo={
                            "code":page.movie["code"],
                            "studio":page.series
                        }
                        starCategoryVo={
                            "stars":page.stars,
                            "categories":page.categories
                        }
                        starDirectorVo={
                            "stars":page.stars,
                            "director":page.director
                        }
                        starStudioVo={
                            "stars":page.stars,
                            "studio":page.studio
                        }
                        starSeriesVo={
                            "stars":page.stars,
                            "series":page.series
                        }
                        self.sendData2Server(movieBigImageVo,"/movie/relation/bigimage/save")
                        self.sendData2Server(movieCategoryVo,"/movie/relation/category/save")
                        self.sendData2Server(movieDirectVo,"/movie/relation/director/save")
                        self.sendData2Server(movieLabelVo,"/movie/relation/label/save")
                        self.sendData2Server(movieStarVo,"/movie/relation/star/save")
                        self.sendData2Server(movieSampleImageVo,"/movie/relation/sampleimage/save")
                        self.sendData2Server(movieStudioVo,"/movie/relation/studio/save")
                        self.sendData2Server(movieSeriesVo,"/movie/relation/series/save")
                        self.sendData2Server(starCategoryVo,"/star/relation/category/save")
                        self.sendData2Server(starDirectorVo,"/star/relation/director/save")
                        self.sendData2Server(starStudioVo,"/star/relation/studio/save")
                        self.sendData2Server(starSeriesVo,"/star/relation/series/save")
            print("all link was visited jump to next page")
        else:
            print("page list not found")
    def save2local(self,content,path):
        with open(path+".json","w",encoding="UTF-8") as f:
            json.dump(content,f,ensure_ascii=False)
    def sendData2Server(self,data,path):
        response=self.RequestUtil.post(data=data,path=path)
        if response.status_code==200:
            print("send "+str(data)+" to "+path+" was success")
        else:
            print("send "+str(data)+" to "+path+" was failure")