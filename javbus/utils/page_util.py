import hashlib
import threading
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from javbus.utils.attrs_util import AttrsUtil
from javbus.utils.image_util import ImageUtil
from javbus.utils.log_util import LogUtil
from javbus.utils.actress_util import ActressUtil
from javbus.utils.request_util import RequestUtil
from javbus.utils.timeout_util import TimeoutUtil
from javbus.utils.web_util import WebUtil
from javbus.utils.attrs.company_links import CompanyLinks
from javbus.items import (
    DirectorItem,
    MovieItem,
    PageItem,
    SampleImageItem,
    StudioItem,
    SeriesItem,
    LabelItem,
    MagnetItem,
    BigImageItem,
)


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

    def __init__(self) -> None:
        pass

    def parseDetailPage(self, link, is_censored):
        """解析电影详情页"""
        self.logUtil.log("sleeping in 10 seconds")
        time.sleep(10)
        source = self.webUtil.get(link, True)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            page = self.getPage(bs, is_censored)
            if page != -1:
                page.movie["link"] = link
                actresses = page.actresses
                code = page.movie.get("code")
                # 女演员名字的集合
                names = (
                    [actress.get("name") for actress in actresses] if actresses else []
                )
                return page
            else:
                return -1
        else:
            self.logUtil.log("request " + link + " timeout")
            return None

    def getSampleImageLinks(self, page):
        """获取样品图像链接集合"""
        links = []
        if page.sampleimage:
            for sample in page.sampleimage:
                for link in sample:
                    links.append(sample[link])
        return links

    def getPage(self, bs, is_censored):
        """从 BeautifulSoup 中获取页面数据"""
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
        actressesList = self.getActresses(bs, is_censored)

        # 获取种子链接
        magnets = self.getMagnets(bs)

        # 填充 PageItem 对象
        page = self.fillPageData(
            page,
            bigimage,
            movie,
            director,
            series,
            studio,
            label,
            actressesList,
            samples,
            magnets,
        )

        return page

    '''
    def getBigImageLink(self, bs):
        """获取大图链接"""
        # 查找类名为 "bigImage" 的 <a> 标签
        a = bs.find("a", {"class": "bigImage"})

        if a:
            # 从该 <a> 标签获取大图链接
            bigImageLink = self.attrsUtil.getBigImage(a)

            # 检查大图链接是否为公司链接
            is_company_link = self.matchLinkIsCompanyLink(bigImageLink)

            if is_company_link:
                return bigImageLink
            else:
                # 拼接基础 URL 和大图链接
                return self.baseUrl + bigImageLink

        # 如果没有找到符合条件的 <a> 标签，返回空字符串
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
    '''

    def getMovieInfo(self, bs, movie, director, studio, label, series):
        """获取电影信息"""
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
                        director.name, director.link = list(
                            self.attrsUtil.getDirector(p).items()
                        )[0]
                    if "製作商:" in header:
                        studio.name, studio.link = list(
                            self.attrsUtil.getStudio(p).items()
                        )[0]
                    if "發行商:" in header:
                        label.name, label.link = list(
                            self.attrsUtil.getLabel(p).items()
                        )[0]
                    if "系列:" in header:
                        series.name, series.link = (
                            list(self.attrsUtil.getSeries(p).items())[0]
                            if self.attrsUtil.getSeries(p)
                            else ("", "")
                        )

    def getActresses(self, bs, is_censored):
        """获取所有的女演员信息"""
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            actresses = self.attrsUtil.getActresses(ps[-1])
            return actresses
        return None 

    def getMagnets(self, bs):
        """获取种子链接"""
        magnetLinks = self.attrsUtil.getMagnets(bs)
        magnets = []
        if magnetLinks:
            for link in magnetLinks:
                m = MagnetItem()
                m.name, m.link, m.size, m.share_date = (
                    link["name"],
                    link["link"],
                    link["size"],
                    link["share_date"],
                )
                magnets.append(m.toDict())
        return magnets

    def matchLinkIsCompanyLink(self, link):
        """检查链接是否属于公司"""
        for company in self.companys.values:
            if company in link:
                return True
        return False

    def fillPageData(
        self,
        page,
        bigimage,
        movie,
        director,
        series,
        studio,
        label,
        actressesList,
        samples,
        magnets,
    ):
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
