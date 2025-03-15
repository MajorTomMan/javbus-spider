import logging
from javbus.utils.attrs.ban_list import Ban

class AttrsUtil:
    ban = Ban()
    logger = logging.getLogger(__name__)  # 使用 Scrapy 的日志系统

    def __init__(self):
        self.logger.setLevel(logging.INFO)  # 设置日志级别

    def get_title(self, bs):
        h3 = bs.find("h3")
        if h3:
            title = h3.text
            return title
        else:
            self.logger.warning("title not found")
            return None

    def get_big_image(self, bs):
        imgs = bs.find("img")
        if imgs:
            img = imgs["src"]
            return img
        else:
            self.logger.warning("img not found")
            return None

    def get_sample_images(self, bs):
        sampleImgs = []
        boxs = bs.find_all("a", {"class": "sample-box"})
        if boxs:
            for box in boxs:
                href = box["href"]
                sampleImgs.append(href)
            return sampleImgs
        else:
            self.logger.warning("sampleImage not found")

    def get_code(self, bs):
        span = bs.find("span", {"style": "color:#CC0000;"})
        if span:
            code = span.text.strip()
            return code
        else:
            self.logger.warning("code not found")
            return None

    def get_release_date(self, bs):
        return bs.next_sibling.text.strip()

    def get_length(self, bs):
        return bs.next_sibling.text.strip()

    def get_director_info(self, bs):
        director = {}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text.strip()
            director[name] = href
            return director
        else:
            self.logger.warning("director not found")
            return None

    def get_studio_info(self, bs):
        studio = {}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text.strip()
            studio[name] = href
            return studio
        else:
            self.logger.warning("studio not found")
            return None

    def get_label_info(self, bs):
        labels = {}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text.strip()
            labels[name] = href
            return labels
        else:
            self.logger.warning("label not found")
            return None

    def get_genres(self, bs):
        genres = []
        genreList = bs.find_all("span", {"class": "genre"})
        if genreList:
            for genre in genreList:
                a = genre.find("a")
                if a:
                    tag = a.text.strip()
                    if tag in self.ban.tags:
                        self.logger.warning("found ban tag in movie")
                        return -1
            for genre in genreList:
                temp = {}
                a = genre.find("a")
                if a:
                    temp = {}
                    tag = a.text.strip()
                    temp["name"] = tag
                    href = a["href"]
                    temp["link"] = href
                    genres.append(temp)
            return genres
        else:
            self.logger.warning("genres not found")
            return None

    def get_categories(self, bs):
        categories = []
        ass = bs.find_all("a")
        if ass:
            for a in ass:
                temp = {}
                tag = a.text.strip()
                temp["name"] = tag
                href = a["href"]
                temp["link"] = href
                categories.append(temp)
            return categories
        else:
            self.logger.warning("categories not found")
            return None

    def get_actress_list(self, bs):
        names = []
        spans = bs.find_all("span", {"class": "genre"})
        if spans:
            for span in spans:
                a = span.find("a")
                if a:
                    temp = {}
                    link = a["href"]
                    name = a.text
                    temp["name"] = name
                    temp["link"] = link
                    names.append(temp)
            return names
        else:
            self.logger.warning("actresses not found")
            return None

    def get_series_info(self, bs):
        series = {}
        a = bs.find("a")
        if a:
            href = a["href"]
            serie = a.text
            series[serie] = href
            return series
        else:
            self.logger.warning("series not found")
            return None

    def get_photo_link(self, bs):
        img = bs.find("img")
        if img:
            src = img["src"]
            return src

    def get_birth_day(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_age(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_height(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_cup_size(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_bust_size(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_waist_size(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_hip_size(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_birth_place(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_hobby(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def get_name(self, bs):
        span = bs.find("span", {"class": "pb10"})
        if span:
            name = span.text
            return name.strip()
        else:
            self.logger.warning("name not found")
            return None


    def get_magnets(self, bs):
        magnets = []
        trs = bs.find_all("tr")
        if trs:
            for tr in trs:
                temp = {}
                tds = tr.find_all("td")
                if tds:
                    a = tds[0].find("a")
                    if a:
                        temp["name"] = a.text.strip()
                        temp["link"] = a["href"]
                        a = tds[1].find("a")
                        if a:
                            temp["size"] = a.text.strip()
                        a = tds[2].find("a")
                        if a:
                            temp["share_date"] = a.text.strip()
                        magnets.append(temp)
            return magnets
        else:
            return None

    def str_to_bool(self,value):
            if isinstance(value, bool): 
                return value
            if isinstance(value, str): 
                value = value.strip().lower()
                if value in ["true", "1", "t", "y", "yes"]:
                    return True
                elif value in ["false", "0", "f", "n", "no"]:
                    return False
            return bool(value)  # 默认转换成布尔值（比如数字 0 或空字符串会转为 False，其他会转为 True）

