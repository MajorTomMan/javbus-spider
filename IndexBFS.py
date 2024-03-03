from bs4 import BeautifulSoup

from utils.Utils import AttrsUtil, WebUtil, ImageUtil


class index:
    def __init__(self,url):
        self.imageUtil=ImageUtil()
        self.attrsUtil=AttrsUtil()
        self.webUtil=WebUtil()
        self.links = []
        self.imgLinks = []
        self.directors = {}
        self.sample_dict = {}
        self.studios = {}
        self.labels = {}
        self.genres = {}
        self.names = {}
        self.infos = []
        self.series = {}
        self.pageNum = 1

        self.baseUrl = url
        #self.searchUrl = self.baseUrl + "/search/"

        #self.unknownNamePath = "../图片/未知名字/"
        #self.storeImagePath = "../图片/"

        #self.searchActors = ["北野未奈", "安斋らら", "藤森里穗"]

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
                    self.__parseDetailPage(link)
                break
            print("all link was visited jump to next page")
        else:
            print("movie list not found")
    def __parseDetailPage(self, link):
        driver = self.webUtil.getWebSite(link)
        bs = BeautifulSoup(driver.page_source,"html.parser")
        title = self.attrsUtil.getTitle(bs)
        infos = self.getInfos(bs)
        a = bs.find("a", {"class": "bigImage"})
        if a:
            bigImagePath=self.attrsUtil.getBigImage(a,self.baseUrl)
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            name = infos["演員"]
            imgs = self.attrsUtil.getSampleImages(waterfall)
            if imgs:
                if infos:
                    self.sample_dict[name] = imgs
                else:
                    self.sample_dict[title] = imgs
        self.imageUtil.downloadSampleImages(links=self.sample_dict[name],info=infos)
        self.imageUtil.downloadBigImage(bigImagePath,info=infos)
        for k, v in infos.items():
            print(k + ":" + v)
    def getInfos(self, bs):
        infoDict = {}
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.attrsUtil.getCode(p)
                        infoDict["識別碼"] = code
                    if "發行日期:" in header:
                        date = self.attrsUtil.getReleaseDate(header)
                        infoDict["發行日期"] = date
                    if "長度:" in header:
                        length = self.attrsUtil.getLength(header)
                        infoDict["長度"] = length
                    if "導演:" in header:
                        director = self.attrsUtil.getDirector(p,self.directors)
                        infoDict["導演"] = director
                    if "製作商:" in header:
                        studio = self.attrsUtil.getStudio(p,self.studios)
                        infoDict["製作商"] = studio
                    if "發行商:" in header:
                        label = self.attrsUtil.getLabel(p,self.labels)
                        infoDict["發行商"] = label
                    if "系列:" in header:
                        series = self.attrsUtil.getSeries(p,self.series)
                        if series:
                            infoDict["系列"] = series
                        else:
                            print("series not found")

            p=ps[-3]
            genres = self.attrsUtil.getGenres(p,self.genres)
            infoDict["類別"] = genres
            p = ps[-1]
            name = self.attrsUtil.getName(p,self.names)
            if name:
                infoDict["演員"] = name
            return infoDict
        else:
            print("info not found")
            return None