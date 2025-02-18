import logging
from javbus.utils.attrs.ban_list import Ban

class AttrsUtil:
    ban = Ban()
    logger = logging.getLogger(__name__)  # 使用 Scrapy 的日志系统

    def __init__(self):
        self.logger.setLevel(logging.INFO)  # 设置日志级别

    def getLink(self, bs):
        a = bs.find("a", {"class": "movie-box"})
        if a:
            link = a["href"]
            return link
        a = bs.find("a", {"class": "avatar-box text-center"})
        if a:
            link = a["href"]
            return link
        self.logger.warning("singer movie link not found, skip")
        return None

    def getTitle(self, bs):
        h3 = bs.find("h3")
        if h3:
            title = h3.text
            return title
        else:
            self.logger.warning("title not found")
            return None

    def getBigImage(self, bs):
        imgs = bs.find("img")
        if imgs:
            img = imgs["src"]
            return img
        else:
            self.logger.warning("img not found")
            return None

    def getSampleImages(self, bs):
        sampleImgs = []
        boxs = bs.find_all("a", {"class": "sample-box"})
        if boxs:
            for box in boxs:
                href = box["href"]
                sampleImgs.append(href)
            return sampleImgs
        else:
            self.logger.warning("sampleImage not found")

    def getCode(self, bs):
        span = bs.find("span", {"style": "color:#CC0000;"})
        if span:
            code = span.text.strip()
            return code
        else:
            self.logger.warning("code not found")
            return None

    def getReleaseDate(self, bs):
        return bs.next_sibling.text.strip()

    def getLength(self, bs):
        return bs.next_sibling.text.strip()

    def getDirector(self, bs):
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

    def getStudio(self, bs):
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

    def getLabel(self, bs):
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

    def getGenres(self, bs):
        genres = []
        genreList = bs.find_all("span", {"class": "genre"})
        if genreList:
            # 查找目标影片是否含有禁止的分类
            for genre in genreList:
                a = genre.find("a")
                if a:
                    tag = a.text.strip()
                    if tag in self.ban.tags:
                        self.logger.warning("found ban tag in movie")
                        return -1
            for genre in genreList:
                temp={}
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

    def getCategories(self, bs):
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

    def getActresses(self, bs):
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

    def getSeries(self, bs):
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

    def getPhotoLink(self, bs):
        img = bs.find("img")
        if img:
            src = img["src"]
            return src

    def getBirthDay(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getAge(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getHeight(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getCup(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getBust(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getWaist(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getHip(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getBirthPlace(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getHobby(self, bs):
        attr = bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getName(self, bs):
        span = bs.find("span", {"class": "pb10"})
        if span:
            name = span.text
            return name.strip()
        else:
            self.logger.warning("name not found")
            return None

    def getSingleActressLink(self, bs):
        box = bs.find("a", {"class": "avatar-box text-center"})
        if box:
            img = box.find("img")
            if img:
                name = img["title"]
                photo_link = img["src"]
                return {
                    "name": name,
                    "photo_link": photo_link,
                    "actress_link": box["href"],
                }
        else:
            self.logger.warning("page actresses not found")
            return None

    def getIsCensored(self, bs):
        button = bs.find("button", {"class": "btn btn-xs btn-info"})
        if button:
            if "有碼" in button.text.strip():
                return True
            elif "无碼" in button.text.strip():
                return False

    def getMagnets(self, bs):
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


    def str_to_bool(self, value):
        if type(value) is str:
            return value.lower() == "true"
        return value
