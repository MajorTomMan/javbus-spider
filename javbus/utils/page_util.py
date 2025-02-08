import hashlib
import threading
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.attrs_util import AttrsUtil
from utils.image_util import ImageUtil
from utils.log_util import LogUtil
from utils.actress_util import ActressUtil
from utils.request_util import RequestUtil
from utils.timeout_util import TimeoutUtil
from utils.web_util import WebUtil
from utils.attrs.company_links import CompanyLinks
from items import DirectorItem, MovieItem, PageItem, SampleImageItem, StudioItem, SeriesItem, LabelItem, MagnetItem, BigImageItem


class PageUtil:
    webUtil = WebUtil()
    imageUtil = ImageUtil()
    attrsUtil = AttrsUtil()
    actressUtil = ActressUtil()
    logUtil = LogUtil()
    companys = CompanyLinks()
    lock = threading.Lock()
    requestUtil = RequestUtil()
    timeoutUtil = None

    def __init__(self, url) -> None:
        self.baseUrl = url

    def parseDetailPage(self, link, isCensored):
        """ 解析电影详情页 """
        self.logUtil.log("sleeping in 10 seconds")
        time.sleep(10)
        source = self.webUtil.get(link, True)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            page = self.getPage(bs, isCensored)
            if page != -1:
                page.movie["link"] = link
                actresses = page.actresses
                code = page.movie.get("code")
                # 样品图像的链接集合
                links = self.getSampleImageLinks(page)
                # 女演员名字的集合
                names = [actress.get("name") for actress in actresses] if actresses else []
                # 处理图像下载
                self.handleImages(page, links, names, code)
                return page
            else:
                return -1
        else:
            self.logUtil.log("request " + link + " timeout")
            return None

    def getSampleImageLinks(self, page):
        """ 获取样品图像链接集合 """
        links = []
        if page.sampleimage:
            for sample in page.sampleimage:
                for link in sample:
                    links.append(sample[link])
        return links

    def handleImages(self, page, links, actresses, code):
        """ 处理图像下载 """
        try:
            if links and len(links) >= 1:
                self.imageUtil.downloadSampleImages(links=links, actresses=actresses, code=code)
            if page.bigimage and page.bigimage.get("link"):
                self.imageUtil.downloadBigImage(link=page.bigimage["link"], actresses=actresses, code=code)
        except Exception as e:
            self.logUtil.log("-------------image error info actresses------------------")
            self.logUtil.log(f"Error while downloading images: {e}")
            self.logUtil.log(f"Failed page details: {page}")
            self.logUtil.log("-------------image error info end------------------")

    def getPage(self, bs, isCensored):
        """ 从 BeautifulSoup 中获取页面数据 """
        page = PageItem()
        bigimage = BigImageItem()
        movie = MovieItem()
        director = DirectorItem()
        series = SeriesItem()
        studio = StudioItem()
        label = LabelItem()
        actressesList = []
        samples = []
        magnets = []

        # 解析电影标题
        title = self.attrsUtil.getTitle(bs)
        if title:
            movie.title = title

        # 获取大图链接
        bigimage.link = self.getBigImageLink(bs)

        # 获取样品图像链接
        self.getSampleImages(bs, samples)

        # 获取电影信息（如代码、发行日期、导演等）
        self.getMovieInfo(bs, movie, director, studio, label, series)

        # 获取女演员信息
        actressesList = self.getActresses(bs, isCensored)

        # 获取种子链接
        magnets = self.getMagnets(bs)

        # 填充 PageItem 对象
        page = self.fillPageData(page, bigimage, movie, director, series, studio, label, actressesList, samples, magnets)

        return page

    def getBigImageLink(self, bs):
        """ 获取大图链接 """
        a = bs.find("a", {"class": "bigImage"})
        if a:
            bigImageLink = self.attrsUtil.getBigImage(a)
            return self.matchLinkIsCompanyLink(bigImageLink) and bigImageLink or self.baseUrl + bigImageLink
        return ""

    def getSampleImages(self, bs, samples):
        """ 获取样品图像 """
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.attrsUtil.getSampleImages(waterfall)
            if imgs:
                for img in imgs:
                    sample = SampleImageItem()
                    sample.link = self.matchLinkIsCompanyLink(img) and img or self.baseUrl + img
                    samples.append(sample.toDict())

    def getMovieInfo(self, bs, movie, director, studio, label, series):
        """ 获取电影信息 """
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        movie.code = self.attrsUtil.getCode(p)
                    if "發行日期:" in header:
                        movie.release_date = self.attrsUtil.getReleaseDate(header)
                    if "長度:" in header:
                        movie.length = self.attrsUtil.getLength(header)
                    if "導演:" in header:
                        director.name, director.link = list(self.attrsUtil.getDirector(p).items())[0]
                    if "製作商:" in header:
                        studio.name, studio.link = list(self.attrsUtil.getStudio(p).items())[0]
                    if "發行商:" in header:
                        label.name, label.link = list(self.attrsUtil.getLabel(p).items())[0]
                    if "系列:" in header:
                        series.name, series.link = list(self.attrsUtil.getSeries(p).items())[0] if self.attrsUtil.getSeries(p) else ("", "")

    def getActresses(self, bs, isCensored):
        """ 获取女演员信息 """
        actressesList = []
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            actresses = self.attrsUtil.getActresses(ps[-1])
            if actresses:
                for actress in actresses:
                    actressDetail = self.actressUtil.getActressDetails(actresses[actress])
                    if actressDetail:
                        actressDetail.actress_link = actresses.get(actress)
                        actressDetail.is_censored = isCensored
                        actressesList.append(actressDetail.toDict())
        return actressesList

    def getMagnets(self, bs):
        """ 获取种子链接 """
        magnetLinks = self.attrsUtil.getMagnets(bs)
        magnets = []
        if magnetLinks:
            for link in magnetLinks:
                m = MagnetItem()
                m.name, m.link, m.size, m.share_date = link["name"], link["link"], link["size"], link["share_date"]
                magnets.append(m.toDict())
        return magnets

    def matchLinkIsCompanyLink(self, link):
        """ 检查链接是否属于公司 """
        for company in self.companys.values:
            if company in link:
                return True
        return False

    def fillPageData(self, page, bigimage, movie, director, series, studio, label, actressesList, samples, magnets):
        page.bigimage = bigimage
        page.movie = movie
        page.director = director
        page.series = series
        page.studio = studio
        page.label = label
        page.actresses = actressesList
        page.sampleimage = samples
        page.magnets = magnets
        return page
