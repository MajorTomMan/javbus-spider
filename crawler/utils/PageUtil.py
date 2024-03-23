import hashlib
import threading
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup


from utils.AttrsUtil import AttrsUtil
from utils.ImageUtil import ImageUtil
from utils.LogUtil import LogUtil
from utils.ActressUtil import ActressUtil
from utils.RequestUtil import RequestUtil
from utils.TimeoutUtil import TimeoutUtil
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
    companys = CompanyLinks()
    lock = threading.Lock()
    requestUtil = RequestUtil()
    timeoutUtil = None

    def __init__(self, url) -> None:
        self.baseUrl = url

    def parseDetailPage(self, link, isCensored):
        self.logUtil.log("sleeping in 10 seconds")
        time.sleep(10)
        source = self.webUtil.getWebSite(link)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            page = self.getPage(bs, isCensored)
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
                try:
                    if links and len(links) >= 1:
                        self.imageUtil.downloadSampleImages(
                            links=links, actresses=names, code=code
                        )
                    if page.bigimage["link"]:
                        self.imageUtil.downloadBigImage(
                            link=page.bigimage["link"], actresses=names, code=code
                        )
                except Exception as e:
                    self.logUtil.log(
                        "-------------image error info actresst------------------"
                    )
                    self.logUtil.log("Error while downloading images: ")
                    self.logUtil.log(e)
                    self.logUtil.log("Failed page details: ")
                    self.logUtil.log(page)
                    self.logUtil.log(
                        "-------------image error info end------------------"
                    )
                return page
            else:
                return -1
        else:
            self.logUtil.log("request " + link + " timeout")
            return None

    def getPage(self, bs, isCensored):
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
                        actressDetail.is_censored = isCensored
                        actressesList.append(actressDetail.toDict())
            if actresses:
                p = ps[-3]
            else:
                p = ps[-2]
            genres = self.attrsUtil.getGenres(p)
            if genres and genres != -1:
                categories = []
                for k, v in genres.items():
                    categories.append({"name": k, "link": v, "is_censored": isCensored})
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
            movie.is_censored = isCensored
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

    def parseMovieListPage(self, link, isCensored):
        source = self.webUtil.getWebSite(link)
        if not source:
            if self.timeoutUtil is None:
                self.timeoutUtil = TimeoutUtil(self)
            self.timeoutUtil.addLink(link, isCensored)
            return True
        bs = BeautifulSoup(source, "html.parser")
        bricks = bs.find_all("div", attrs={"class": "item masonry-brick"})
        if bricks:
            for brick in bricks:
                try:
                    url = self.attrsUtil.getLink(brick)
                    if url:
                        # 如果电影页存在
                        page = self.parseDetailPage(url, isCensored)
                        if page and page != -1:
                            self.sendData2Server(page)
                        elif page == -1:
                            continue
                        else:
                            self.logUtil.log("add " + url + " to timeouts")
                            self.timeoutUtil.addLink(link, isCensored)
                except Exception as e:
                    self.logUtil.log(e)
            self.logUtil.log("all link was visited jump to next page")
            if self.hasNextPage(bs):
                return False
            else:
                return True
        else:
            self.logUtil.log("bricks not found")
            self.logUtil.log("save error page to local")
            self.save2local(source, link, ".html")

    def save2local(self, content, link, extensions):
        # 获取链接的路径名
        parsed_url = urlparse(link)
        path_name = parsed_url.path.replace("/", "_")
        # 计算路径名的哈希值
        hash_value = hashlib.md5(path_name.encode()).hexdigest()

        # 构建保存文件的路径
        save_path = f"./failed_link/{path_name}_{hash_value}{extensions}"
        with open(save_path, "w+", encoding="UTF-8") as f:
            f.write(content)

    def sendData2Server(self, page):
        if page.movie and len(page.movie) >= 1:
            self.requestUtil.send(page.movie, "/movie/save")
        if page.bigimage and len(page.bigimage) >= 1:
            movieBigImageVo = {
                "movie": page.movie,
                "bigImage": page.bigimage,
            }
            self.requestUtil.send(movieBigImageVo, "/movie/relation/bigimage/save")
        if page.categories and len(page.categories) >= 1:
            movieCategoryVo = {"movie": page.movie, "categories": page.categories}
            self.requestUtil.send(movieCategoryVo, "/movie/relation/category/save")
        if page.director and len(page.director) >= 1:
            movieDirectVo = {"movie": page.movie, "director": page.director}
            self.requestUtil.send(movieDirectVo, "/movie/relation/director/save")
        if page.label and len(page.label) >= 1:
            movieLabelVo = {"movie": page.movie, "label": page.label}
            self.requestUtil.send(movieLabelVo, "/movie/relation/label/save")
        if page.sampleimage and len(page.sampleimage) >= 1:
            movieSampleImageVo = {"movie": page.movie, "sampleImages": page.sampleimage}
            self.requestUtil.send(
                movieSampleImageVo, "/movie/relation/sampleimage/save"
            )
        if page.actresses and len(page.actresses) >= 1:
            if page.director:
                actressDirectorVo = {
                    "actress": page.actresses,
                    "director": page.director,
                }
                self.requestUtil.send(
                    actressDirectorVo, "/actress/relation/director/save"
                )
            if page.studio:
                actressStudioVo = {"actress": page.actresses, "studio": page.studio}
                self.requestUtil.send(actressStudioVo, "/actress/relation/studio/save")
            if page.series:
                actressSeriesVo = {"actress": page.actresses, "series": page.series}
                self.requestUtil.send(actressSeriesVo, "/actress/relation/series/save")
            if page.movie:
                movieActressVo = {"movie": page.movie, "actress": page.actresses}
                self.requestUtil.send(movieActressVo, "/movie/relation/actress/save")
            if page.categories and len(page.categories) >= 1:
                actressCategoryVo = {
                    "actress": page.actresses,
                    "categories": page.categories,
                }
                self.requestUtil.send(
                    actressCategoryVo, "/actress/relation/category/save"
                )
        if page.studio and len(page.studio) >= 1:
            movieStudioVo = {"movie": page.movie, "studio": page.studio}
            self.requestUtil.send(movieStudioVo, "/movie/relation/studio/save")
        if page.series and len(page.series) >= 1:
            movieSeriesVo = {"movie": page.movie, "series": page.series}
            self.requestUtil.send(movieSeriesVo, "/movie/relation/series/save")

    def printPage(self, page):
        with page.lock:
            self.logUtil.log(
                "------------------------------page info actresst--------------------------------------"
            )
            self.logUtil.log(page)
            self.logUtil.log(
                "------------------------------page info ended--------------------------------------"
            )
            if page.actresses:
                self.logUtil.log(
                    "------------------------------actress info actresst--------------------------------------"
                )
                for actress in page.actresses:
                    self.logUtil.log(actress)
                self.logUtil.log(
                    "------------------------------actress info ended--------------------------------------"
                )
