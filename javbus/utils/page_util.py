import re
import scrapy
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from javbus.utils.attrs_util import AttrsUtil
from javbus.utils.actress_util import ActressUtil
from javbus.utils.request_util import RequestUtil
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
    CategoryItem,
    ActressItem,
)


class PageUtil:
    attrsUtil = AttrsUtil()
    actressUtil = ActressUtil()
    companys = CompanyLinks()
    requestUtil = RequestUtil()
    timeoutUtil = None
    base_url = "https://www.javbus.com"
    big_image_url = "https://pics.dmm.co.jp/mono/movie/adult/"

    def parsePage(self, link, source, is_censored):
        """解析电影详情页"""
        if source:
            page = self.getPage(source, link, is_censored)
            if page != -1:
                page["movie"]["link"] = link
                return page
            else:
                scrapy.logger.error("Request {} timed out".format(link))
                return None
        else:
            scrapy.logger.error("Source for link {} is None".format(link))
            return None

    def getSampleImageLinks(self, page):
        """获取样品图像链接集合"""
        links = []
        if page.sampleimage:
            for sample in page.sampleimage:
                for link in sample:
                    links.append(sample[link])
        return links

    def getPage(self, bs, link, is_censored):
        """从 BeautifulSoup 中获取页面数据"""
        page = PageItem()
        bigimage = BigImageItem()
        movie = MovieItem()
        director = DirectorItem()
        series = SeriesItem()
        studio = StudioItem()
        label = LabelItem()
        categories = CategoryItem()
        actressesList = []
        magnets = []

        # 获取电影信息（如代码、发行日期、导演等）
        self.getMovieInfo(bs, movie, director, studio, label, series)
        movie["is_censored"] = is_censored
        # 获取女演员信息
        actressesList = self.getActresses(bs)

        if actressesList:
            categories = self.getCategories(bs, True, is_censored)
        else:
            categories = self.getCategories(bs, False, is_censored)

        # 发现禁止的tag,该网页放弃爬取
        if categories == -1:
            scrapy.logger.warning(
                "Forbidden category detected, skipping link: {}".format(link)
            )
            return -1

        # 获取种子链接
        magnets = self.getMagnets(bs, link)
        # 获取大图链接
        bigimage["link"] = self.getBigImageLink(bs, movie["code"])

        # 获取样品图像链接
        sampleimages = self.getSampleImages(bs)
        # 填充 PageItem 对象
        page = self.fillPageData(
            page,
            movie,
            director,
            series,
            studio,
            label,
            actressesList,
            categories,
            bigimage,
            sampleimages,
            magnets,
        )

        return page

    def getMovieInfo(self, bs, movie, director, studio, label, series):
        """获取电影信息"""
        title = self.attrsUtil.getTitle(bs)
        if title:
            movie["title"] = title
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.attrsUtil.getCode(p)
                        if code:
                            movie["code"] = code
                    if "發行日期:" in header:
                        date = self.attrsUtil.getReleaseDate(header)
                        if date:
                            movie["release_date"] = date
                    if "長度:" in header:
                        length = self.attrsUtil.getLength(header)
                        if length:
                            movie["length"] = length
                    if "導演:" in header:
                        d = self.attrsUtil.getDirector(p)
                        if d:
                            director["name"] = list(d.keys())[0]
                            director["link"] = d.get(director["name"])
                    if "製作商:" in header:
                        s = self.attrsUtil.getStudio(p)
                        if s:
                            studio["name"] = list(s.keys())[0]
                            studio["link"] = s.get(studio["name"])
                    if "發行商:" in header:
                        l = self.attrsUtil.getLabel(p)
                        if l:
                            label["name"] = list(l.keys())[0]
                            label["link"] = l.get(label["name"])
                    if "系列:" in header:
                        s = self.attrsUtil.getSeries(p)
                        if s:
                            series["name"] = list(s.keys())[0]
                            series["link"] = s.get(series["name"])
                        else:
                            scrapy.logger.warning(
                                "Series not found for movie code: {}".format(
                                    movie.get("code")
                                )
                            )

    def getActresses(self, bs):
        """获取所有的女演员信息"""
        actresses = []
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            actressList = self.attrsUtil.getActresses(ps[-1])
            if actressList:
                for actress in actressList:
                    temp = ActressItem()
                    temp["actress_link"] = actress["link"]
                    temp["name"] = actress["name"]
                    actresses.append(temp)
            return actresses
        return None

    def getCategories(self, bs, has_actresses, is_censored):
        temp = []
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            if has_actresses:
                temp = self.attrsUtil.getGenres(ps[-3], is_censored)
            else:
                temp = self.attrsUtil.getGenres(ps[-2], is_censored)
        return temp

    def getMagnets(self, bs, link):
        # 找到所有 <script> 标签
        scripts = bs.find_all("script")
        gid, uc, img = self.get_magnet_parameters(scripts)
        base_url = self.extract_domain_with_https(link)
        if self.check_parameters(gid, uc, img):
            magnet_reponse = self.requestUtil.sendMangets(base_url, gid, img, uc, link)
            if magnet_reponse:
                # 解析 JavaScript 返回的 HTML 内容
                magnet_link = BeautifulSoup(magnet_reponse.content, "html.parser")
                # 获取磁力链接
                links = self.attrsUtil.getMagnets(magnet_link)
                items = self.build_magnet_items(links)
                return items
            scrapy.logger.error("Failed to get magnet link for: {}".format(link))
            return None

    def build_magnet_items(self, links):
        magnets = []
        if links:
            for link in links:
                magnet = MagnetItem()
                magnet["name"] = link["name"]
                magnet["link"] = link["link"]
                magnet["size"] = link["size"]
                magnet["share_date"] = link["share_date"]
                magnets.append(magnet)
        return magnets

    def get_magnet_parameters(self, scripts):
        # 初始化参数
        gid, uc, img = None, None, None
        # 从 <script> 标签中提取参数
        for script in scripts:
            if script.string:
                match_gid = re.search(r"var gid = (\d+);", script.string)
                match_uc = re.search(r"var uc = (\d+);", script.string)
                match_img = re.search(r"var img = '(.*?)';", script.string)
                if match_gid:
                    gid = match_gid.group(1)
                if match_uc:
                    uc = match_uc.group(1)
                if match_img:
                    img = match_img.group(1)
        return gid, uc, img

    def check_parameters(self, gid, uc, img):
        if gid is None or uc is None or img is None:
            scrapy.logger.error(
                "Missing parameters: gid:{} uc:{} img:{}".format(gid, uc, img)
            )
            return False
        return True

    def matchLinkIsCompanyLink(self, link):
        """检查链接是否属于公司"""
        for company in self.companys.values:
            if company in link:
                return True
        return False

    def getBigImageLink(self, bs, code):
        if code:
            url = self.big_image_url + code + "/" + code + "pl.jpg"
            response = self.requestUtil.get(url)
            if response.status_code == 200:
                return url
            else:
                a = bs.find("a", {"class": "bigImage"})
                if a:
                    link = self.attrsUtil.getBigImage(a)
                    is_company_link = self.matchLinkIsCompanyLink(link)
                    if is_company_link:
                        return bigImageLink
                    else:
                        return self.base_url + link
        return ""

    def getSampleImages(self, bs):
        samples = []
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.attrsUtil.getSampleImages(waterfall)
            if imgs:
                for img in imgs:
                    sample = SampleImageItem()
                    sample["link"] = (
                        self.matchLinkIsCompanyLink(img) and img or self.base_url + img
                    )
                    samples.append(sample)
        return samples

    def fillPageData(
        self,
        page,
        movie,
        director,
        series,
        studio,
        label,
        actressesList,
        categories,
        bigimage,
        sampleimages,
        magnets,
    ):
        page["movie"] = movie
        page["director"] = director
        page["series"] = series
        page["studio"] = studio
        page["label"] = label
        page["actresses"] = actressesList
        page["categories"] = categories
        page["bigimage"] = bigimage
        page["sampleimage"] = sampleimages
        page["magnets"] = magnets
        return page

    def hasNextPage(self, bs):
        next_button = bs.find("a", id="next")
        if next_button:
            return True
        return False

    def get_backup_links(self, bs):
        backup_links = []
        alert = bs.find(
            "div", {"class": "alert alert-info alert-dismissable alert-common"}
        )
        if alert:
            rows = alert.find_all("a")[1:]
            if rows:
                print("found back links")
                for row in rows:
                    link = row["href"]
                    backup_links.append(link)
                return backup_links
            else:
                print("couldnt found back links")
                return None
        else:
            return None

    def extract_domain_with_https(self,url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc  # 提取域名部分
        return f"https://{domain}"  # 拼接 https://
