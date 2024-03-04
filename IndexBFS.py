from bs4 import BeautifulSoup
from Attr import MovieAttrs

from utils.Utils import AttrsUtil, WebUtil, ImageUtil


class index:
    imageUtil=ImageUtil()
    attrsUtil=AttrsUtil()
    webUtil=WebUtil()
    links=[]
    attrsList=[]
    pageNum = 1
    baseUrl=""
    def __init__(self,url):
        self.baseUrl = url

    def BFS(self):
        if self.baseUrl:
            while(self.pageNum<5):
                driver=self.webUtil.getWebSite(self.baseUrl+"/page/"+str(self.pageNum))
                print("现在正在第"+str(self.pageNum)+"页")
                if self.webUtil.checkisLimitedByAge(driver.title):
                    return
                self.__bfs(driver)
                break
            print("bfs done")
    def __bfs(self,driver):
        bs=BeautifulSoup(driver.page_source,"html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                link = self.attrsUtil.getLink(brick)
                print("now visit website link is "+link)
                if link:
                    self.links.append(link)
                    attrs=self.__parseDetailPage(link)
                    self.attrsList.append(attrs)
                break
            print("all link was visited jump to next page")
        else:
            print("movie list not found")
    def __parseDetailPage(self, link):
        driver = self.webUtil.getWebSite(link)
        bs = BeautifulSoup(driver.page_source,"html.parser")
        title = self.attrsUtil.getTitle(bs)
        attrs = self.getInfos(bs)
        attrs.title=title
        a = bs.find("a", {"class": "bigImage"})
        if a:
            bigImagePath=self.attrsUtil.getBigImage(a,self.baseUrl)
            attrs.bigImageLink=bigImagePath
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.attrsUtil.getSampleImages(waterfall)
            if imgs:
                if attrs:
                    attrs.sampleImageLinks=imgs
        self.imageUtil.downloadSampleImages(links=attrs.sampleImageLinks,attrs=attrs)
        self.imageUtil.downloadBigImage(bigImagePath,attrs=attrs)
        return attrs
    def getInfos(self, bs):
        attrs=MovieAttrs()
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.attrsUtil.getCode(p)
                        attrs.code=code
                    if "發行日期:" in header:
                        date = self.attrsUtil.getReleaseDate(header)
                        attrs.date=date
                    if "長度:" in header:
                        length = self.attrsUtil.getLength(header)
                        attrs.length=length
                    if "導演:" in header:
                        director = self.attrsUtil.getDirector(p)
                        attrs.director=director
                    if "製作商:" in header:
                        studio = self.attrsUtil.getStudio(p)
                        attrs.studio=studio
                    if "發行商:" in header:
                        label = self.attrsUtil.getLabel(p)
                        attrs.label=label
                    if "系列:" in header:
                        series = self.attrsUtil.getSeries(p)
                        if series:
                            attrs.series={}
                        else:
                            print("series not found")

            p=ps[-3]
            genres = self.attrsUtil.getGenres(p)
            attrs.genres=genres
            p = ps[-1]
            name = self.attrsUtil.getName(p)
            if name:
                for k,v in name.items():
                    attrs.name=k
                    attrs.nameLink=v
            return attrs
        else:
            print("info not found")
            return None