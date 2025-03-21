import re
import logging
from urllib.parse import urlparse, urlunparse, urljoin
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
    TopicImageItem,
)
from javbus.common.constants import (
    javbus_base_url,
    high_quality_image_link,
    normal_image_link,
)


class PageUtil:
    attrs_util = AttrsUtil()
    actress_util = ActressUtil()
    companys = CompanyLinks()
    request_util = RequestUtil()
    base_url = javbus_base_url
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.logger.setLevel(logging.INFO)  # 设置日志级别

    def parse_page(self, link, source, is_censored):
        """解析电影详情页"""
        is_censored = AttrsUtil().str_to_bool(is_censored)
        if source:
            page = self.get_page(source, link, is_censored)
            if page != -1:
                page["movie"]["link"] = link
                return page
            else:
                self.logger.error("Request {} timed out".format(link))
                return None
        else:
            self.logger.error("Source for link {} is None".format(link))
            return None

    def get_sample_image_links(self, page):
        """获取样品图像链接集合"""
        links = []
        if page.sampleimage:
            for sample in page.sampleimage:
                for link in sample:
                    links.append(sample[link])
        return links

    def get_page(self, bs, link, is_censored):
        """从 BeautifulSoup 中获取页面数据"""
        page = PageItem()
        bigimage = BigImageItem()
        movie = MovieItem()
        director = DirectorItem()
        series = SeriesItem()
        studio = StudioItem()
        label = LabelItem()
        categories = CategoryItem()
        topic_image = TopicImageItem()
        actresses_list = []
        magnets = []

        # 获取电影信息（如代码、发行日期、导演等）
        self.get_movie_info(bs, movie, director, studio, label, series)
        movie["is_censored"] = is_censored
        # 获取女演员信息
        actresses_list = self.get_actresses(bs)

        if actresses_list:
            categories = self.get_categories(bs, True)
        else:
            categories = self.get_categories(bs, False)

        # 发现禁止的tag,该网页放弃爬取
        if categories == -1:
            self.logger.warning(
                "Forbidden category detected, skipping link: {}".format(link)
            )
            return categories

        # 获取样品图像链接
        sampleimages = self.get_sample_images(bs)
        # 获取种子链接
        magnets = self.get_magnets(bs, link)
        # 获取大图链接
        images = self.get_topic_and_big_image_link(
            bs, movie["code"], sampleimages, is_censored
        )
        if type(images) is dict:
            bigimage["link"] = images["big_image_link"]
            topic_image["link"] = images["topic_image_link"]
        elif type(images) is str:
            bigimage["link"] = images

        page_args = {
            "movie": movie,
            "director": director,
            "series": series,
            "studio": studio,
            "label": label,
            "actresses": actresses_list,
            "categories": categories,
            "bigimage": bigimage,
            "sampleimages": sampleimages,
            "magnets": magnets,
            "topicimage": topic_image,
        }
        # 填充 PageItem 对象
        page = self.fill_page_data(page, **page_args)

        return page

    def get_movie_info(self, bs, movie, director, studio, label, series):
        """获取电影信息"""
        title = self.attrs_util.get_title(bs)
        if title:
            movie["title"] = title
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.attrs_util.get_code(p)
                        if code:
                            movie["code"] = code
                    if "發行日期:" in header:
                        date = self.attrs_util.get_release_date(header)
                        if date:
                            movie["release_date"] = date
                    if "長度:" in header:
                        length = self.attrs_util.get_length(header)
                        if length:
                            movie["length"] = length
                    if "導演:" in header:
                        d = self.attrs_util.get_director_info(p)
                        if d:
                            director["name"] = list(d.keys())[0]
                            director["link"] = d.get(director["name"])
                    if "製作商:" in header:
                        s = self.attrs_util.get_studio_info(p)
                        if s:
                            studio["name"] = list(s.keys())[0]
                            studio["link"] = s.get(studio["name"])
                    if "發行商:" in header:
                        l = self.attrs_util.get_label_info(p)
                        if l:
                            label["name"] = list(l.keys())[0]
                            label["link"] = l.get(label["name"])
                    if "系列:" in header:
                        s = self.attrs_util.get_series_info(p)
                        if s:
                            series["name"] = list(s.keys())[0]
                            series["link"] = s.get(series["name"])
                        else:
                            self.logger.warning(
                                "Series not found for movie code: {}".format(
                                    movie.get("code")
                                )
                            )

    def get_actresses(self, bs):
        """获取所有的女演员信息"""
        actresses = []
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            actress_list = self.attrs_util.get_actress_list(ps[-1])
            if actress_list:
                for actress in actress_list:
                    temp = ActressItem()
                    temp["actress_link"] = actress["link"]
                    temp["name"] = actress["name"]
                    actresses.append(temp)
            return actresses
        return None

    def get_categories(self, bs, has_actresses):
        temp = []
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            if has_actresses:
                temp = self.attrs_util.get_genres(ps[-3])
            else:
                temp = self.attrs_util.get_genres(ps[-2])
        return temp

    def get_magnets(self, bs, link):
        # 找到所有 <script> 标签
        scripts = bs.find_all("script")
        gid, uc, img = self.get_magnet_parameters(scripts)
        base_url = self.change_links(link)
        if self.check_parameters(gid, uc, img):
            magnet_response = self.request_util.request_magnets(
                base_url, gid, img, uc, link
            )
            if magnet_response:
                # 解析 JavaScript 返回的 HTML 内容
                magnet_link = BeautifulSoup(magnet_response.content, "html.parser")
                # 获取磁力链接
                links = self.attrs_util.get_magnets(magnet_link)
                items = self.build_magnet_items(links)
                return items
            self.logger.error("Failed to get magnet link for: {}".format(link))
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
            self.logger.error(
                "Missing parameters: gid:{} uc:{} img:{}".format(gid, uc, img)
            )
            return False
        return True

    def match_link_is_company_link(self, link):
        """检查链接是否属于公司"""
        for company in self.companys.values:
            if type(link) is str:
                if company in link:
                    return True
            elif type(link) is SampleImageItem:
                if company in link["link"]:
                    return True
        return False

    def get_topic_and_big_image_link(self, bs, code, sampleimages, is_censored):
        if code:
            if sampleimages:
                images= {}
                company_link = None
                # 验证是否是dmm链接
                for sample in sampleimages:
                    is_company_link = self.match_link_is_company_link(sample)
                    if is_company_link:
                        company_link = sample
                        break
                if company_link:
                    high_quality_image_url = self.replace_base_url(
                        company_link["link"], high_quality_image_link
                    )
                    dmm_code = None
                    try:
                        dmm_code = self.get_dmm_movie_code(high_quality_image_url)
                    except Exception as e:
                        self.logger.info(f"match code exception:{e}")
                    if dmm_code:
                        new_high_quality_image_url = self.get_dmm_movie_image(
                            high_quality_image_url,dmm_code
                        )
                        response = self.request_util.get(new_high_quality_image_url)
                        if response and response.status_code == 200:
                            images["big_image_link"] = (
                                new_high_quality_image_url.replace("ps.jpg", "pl.jpg")
                            )
                            images["topic_image_link"] = (
                                new_high_quality_image_url.replace("pl.jpg", "ps.jpg")
                            )
                            return images
                        else:
                            normal_image_url = self.replace_base_url(
                                company_link, normal_image_link
                            )
                            response = self.request_util.get(normal_image_url)
                            if response and response.status_code == 200:
                                images["big_image_link"] = (
                                    high_quality_image_url.replace("ps", "pl")
                                )
                                images["topic_image_link"] = high_quality_image_url
                                return images
                            else:
                                pass
            else:
                self.logger.info("uncensored movie,abondoning to get image on dmm")
            a = bs.find("a", {"class": "bigImage"})
            if a:
                link = self.attrs_util.get_big_image(a)
                is_company_link = self.match_link_is_company_link(link)
                if is_company_link:
                    return link
                else:
                    return urljoin(self.base_url, link)
        return ""

    def get_dmm_movie_image(self, link, code):
        new_image = code + "pl.jpg"
        new_url = link.rsplit("/", 1)[0] + "/" + new_image
        return new_url
    def get_dmm_movie_code(self, link):
        match = re.search(r"video/([^/]+)/", link)
        if match:
            code = match.group(1)
            if code:
                self.logger.info(f"get movie code:{code}")
                return code
            else:
                self.logger.info(f"unable match movie code,give up")
                return None
    def get_sample_images(self, bs):
        samples = []
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.attrs_util.get_sample_images(waterfall)
            if imgs:
                for img in imgs:
                    sample = SampleImageItem()
                    if self.match_link_is_company_link(img):
                        sample["link"] = img
                    else:
                        sample["link"] = urljoin(self.base_url, img)
                    samples.append(sample)
        return samples

    def fill_page_data(self, page, **kwargs):
        for key, value in kwargs.items():
            page[key] = value
        return page

    def has_next_page(self, bs):
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
                self.logger.info("Found backup links")
                for row in rows:
                    link = row["href"]
                    backup_links.append(link)
                return backup_links
            else:
                self.logger.info("Couldn't find backup links")
                return None
        else:
            return None

    def change_links(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc  # 提取域名部分
        return f"https://{domain}"

    def replace_base_url(self, original_url, new_base_url):
        # 判断数据类型
        if isinstance(original_url, dict):    # 字典
            parsed_original = original_url.get("link", "")
        elif isinstance(original_url, SampleImageItem) or isinstance(original_url,BigImageItem):    # Scrapy Item 处理
            parsed_original = original_url.get("link", "")
        elif isinstance(original_url, bytes):  # 字节流
            parsed_original = original_url.decode('utf-8')
        elif original_url is None:             # 空值处理
            parsed_original = ""
        else:                                  # 转为字符串
            parsed_original = original_url
        parsed_original = urlparse(parsed_original)
        new_url = urlunparse(
            (
                parsed_original.scheme,  # 使用新 URL 的 scheme
                new_base_url,  # 使用新 URL 的域名
                parsed_original.path,  # 保留原来的路径
                parsed_original.params,  # 保留原来的 params
                parsed_original.query,  # 保留原来的 query
                parsed_original.fragment,  # 保留原来的 fragment
            )
        )

        return new_url
