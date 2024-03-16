import time
from bs4 import BeautifulSoup


from utils.AttrsUtil import AttrsUtil
from utils.ImageUtil import ImageUtil
from utils.LogUtil import LogUtil
from utils.ActressUtil import ActressUtil
from utils.WebUtil import WebUtil
from utils.attrs.CompanyLinks import CompanyLinks


from utils.attrs.Director import Director
from utils.attrs.Movie import Movie
from utils.attrs.Page import Page
from utils.attrs.SampleImage import SampleImage
from utils.attrs.Studio import Studio
from utils.attrs.Series import Series
from utils.attrs.Label import Label

from utils.attrs.BigImage import BigImage


class PageUtil:
    webUtil = WebUtil()
    imageUtil = ImageUtil()
    attrsUtil = AttrsUtil()
    actressUtil = ActressUtil()
    logUtil = LogUtil()
    baseUrl = ""
    isCensored = ""
    companys = CompanyLinks()

    def __init__(self, url, is_censored) -> None:
        self.baseUrl = url
        self.isCensored = is_censored

    def parseDetailPage(self, link):
        self.logUtil.log("sleeping in 10 seconds")
        time.sleep(10)
        source = self.webUtil.getWebSite(link)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            page = self.getPage(bs)
            if page != -1:
                page.movie["link"] = link
                actresses = page.actresses
                code = page.movie.get("code")
                links = []
                for sample in page.sampleimage:
                    for link in sample:
                        links.append(sample[link])
                names = []
                if actresses:
                    for actress in actresses:
                        names.append(actress.get("name"))
                # try:
                # self.imageUtil.downloadSampleImages(
                #    links=links, actresses=names, code=code
                # )
                # self.imageUtil.downloadBigImage(
                #    link=page.bigimage["link"], actresses=names, code=code
                # )
                # except Exception as e:
                # self.logUtil.log(
                #    "-------------image error info start------------------"
                # )
                # self.logUtil.log("Error while downloading images: ")
                # self.logUtil.log(e)
                # self.logUtil.log("Failed page details: ")
                # self.logUtil.log(page)
                # self.logUtil.log(
                #    "-------------image error info end------------------"
                # )
                return page
            else:
                return -1
        else:
            self.logUtil.log("request " + link + " timeout")
            return None

    def getPage(self, bs):
        page = Page()
        bigimage = BigImage()
        movie = Movie()
        director = Director()
        series = Series()
        studio = Studio()
        label = Label()
        actressesList = []
        samples = []
        title = self.attrsUtil.getTitle(bs)
        if title:
            movie.title = title
        a = bs.find("a", {"class": "bigImage"})
        if a:
            bigImageLink = self.attrsUtil.getBigImage(a)
            if not self.matchLinkIsCompanyLink(bigImageLink):
                if self.baseUrl.endswith("/"):
                    url = self.baseUrl[:-1]
                    bigimage.link = url + bigImageLink
                else:
                    bigimage.link = self.baseUrl + bigImageLink
            else:
                bigimage.link = bigImageLink
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.attrsUtil.getSampleImages(waterfall)
            if imgs:
                for img in imgs:
                    sample = SampleImage()
                    # 防止获取的图片地址来源于Dmm而导致脚本运行错误
                    if not self.matchLinkIsCompanyLink(img):
                        if self.baseUrl.endswith("/"):
                            url = self.baseUrl[:-1]
                            sample.link = url + img
                    else:
                        sample.link = img
                    samples.append(sample.toDict())
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.attrsUtil.getCode(p)
                        movie.code = code
                    if "發行日期:" in header:
                        date = self.attrsUtil.getReleaseDate(header)
                        movie.release_date = date
                    if "長度:" in header:
                        length = self.attrsUtil.getLength(header)
                        movie.length = length
                    if "導演:" in header:
                        d = self.attrsUtil.getDirector(p)
                        director.name = list(d.keys())[0]
                        director.link = d.get(director.name)
                    if "製作商:" in header:
                        s = self.attrsUtil.getStudio(p)
                        studio.name = list(s.keys())[0]
                        studio.link = s.get(studio.name)
                    if "發行商:" in header:
                        l = self.attrsUtil.getLabel(p)
                        label.name = list(l.keys())[0]
                        label.link = l.get(label.name)
                    if "系列:" in header:
                        s = self.attrsUtil.getSeries(p)
                        if s:
                            series.name = list(s.keys())[0]
                            series.link = s.get(series.name)
                        else:
                            self.logUtil.log("series not found")
            p = ps[-1]
            actresses = self.attrsUtil.getActresses(p)
            if actresses:
                for actress in actresses:
                    actressDetail = self.actressUtil.getActressDetails(
                        actresses[actress]
                    )
                    if actressDetail:
                        # 解决演员还没有图片的问题
                        if not self.matchLinkIsCompanyLink(actressDetail.photo_link):
                            if self.baseUrl.endswith("/"):
                                url = self.baseUrl[:-1]
                                actressDetail.photo_link = (
                                    url + actressDetail.photo_link
                                )
                        actressDetail.actress_link = actresses.get(actress)
                        actressDetail.is_censored = self.isCensored
                        actressesList.append(actressDetail.toDict())
            if actresses:
                p = ps[-3]
            else:
                p = ps[-2]
            genres = self.attrsUtil.getGenres(p)
            if genres and genres != -1:
                categories = []
                for k, v in genres.items():
                    categories.append(
                        {"name": k, "link": v, "is_censored": self.isCensored}
                    )
                page.categories = categories
            elif genres == -1:
                self.logUtil.log("skipping this page")
                return -1
        else:
            self.logUtil.log("info not found")
        if series:
            page.series = series.toDict()
        if bigimage:
            page.bigimage = bigimage.toDict()
        if bigimage:
            page.sampleimage = samples
        if movie:
            page.movie = movie.toDict()
        if studio:
            page.studio = studio.toDict()
        if director:
            page.director = director.toDict()
        if label:
            page.label = label.toDict()
        if actressesList:
            page.actresses = actressesList
        return page

    def matchLinkIsCompanyLink(self, link):
        if isinstance(link, str):
            for company in self.companys.values:
                if company in link:
                    return True
        return False

    def hasNextPage(self, bs):
        underline = bs.find("div", {"class": "text-center hidden-xs"})
        if underline:
            ul = underline.find("ul", {"class": "pagination pagination-lg"})
            if ul:
                li = ul.find_all("li")
                if li:
                    for l in li:
                        a = l.find("a", id="next")
                        if a:
                            return True
        self.logUtil.log("this page dont have next page element")
        return False
