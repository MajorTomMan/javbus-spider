from utils.LogUtil import LogUtil
from utils.attrs.BanList import Ban
from utils.WebUtil import WebUtil


class AttrsUtil:
    ban = Ban()
    logUtil = LogUtil()
    webUtil = WebUtil()

    def getLink(self, bs):
        a = bs.find("a", {"class": "movie-box"})
        if a:
            link = a["href"]
            return link
        a = bs.find("a", {"class": "avatar-box text-center"})
        if a:
            link = a["href"]
            return link
        self.logUtil.log("singer movie link not found,skip")
        return None

    def getTitle(self, bs):
        h3 = bs.find("h3")
        if h3:
            title = h3.text
            return title
        else:
            self.logUtil.log("title not found")
            return None

    def getBigImage(self, bs):
        imgs = bs.find("img")
        if imgs:
            img = imgs["src"]
            return img
        else:
            self.logUtil.log("img not found")
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
            self.logUtil.log("sampleImage not found")

    def getCode(self, bs):
        span = bs.find("span", {"style": "color:#CC0000;"})
        if span:
            code = span.text.strip()
            return code
        else:
            self.logUtil.log("code not found")
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
            self.logUtil.log("director not found")
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
            self.logUtil.log("studio not found")
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
            self.logUtil.log("label not found")
            return None

    def getGenres(self, bs):
        genres = {}
        genresList = bs.find_all("span", {"class": "genre"})
        if genresList:
            for genre in genresList:
                a = genre.find("a")
                if a:
                    href = a["href"]
                    tag = a.text.strip()
                    if tag in self.ban.tags:
                        self.logUtil.log("found ban tag in movie")
                        return -1
                    genres[tag] = href
            return genres
        else:
            self.logUtil.log("genres not found")
            return None

    def getCategories(self, bs):
        categories = {}
        ass = bs.find_all("a")
        if ass:
            for a in ass:
                tag = a.text.strip()
                if tag in self.ban.tags:
                    self.logUtil.log("found ban tag skipping")
                    continue
                href = a["href"]
                categories[tag] = href
            return categories
        else:
            self.logUtil.log("categories not found")
            return None

    def getActresses(self, bs):
        names = {}
        spans = bs.find_all("span", {"class": "genre"})
        if spans:
            for span in spans:
                a = span.find("a")
                if a:
                    link = a["href"]
                    name = a.text
                    names[name] = link
            return names
        else:
            self.logUtil.log("actresses not found")
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
            self.logUtil.log("series not found")
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
            self.logUtil.log("name not found")
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
            self.logUtil.log("page actresses not found")
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
        tbody = bs.find_all("tbody")[2]
        if tbody:
            trs = tbody.find_all("tr", attrs={"height": "35px"})
            if trs:
                for tr in trs:
                    magnet = {}
                    tds = tr.find_all("td")
                    if tds:
                        a = tds[0].find("a")
                        if a:
                            magnet["name"] = a.text.strip()
                            magnet["link"] = a["href"]
                        a = tds[1].find("a")
                        if a:
                            magnet["size"] = a.text.strip()
                        a = tds[2].find("a")
                        if a:
                            magnet["share_date"] = a.text.strip()
                        magnets.append(magnet)
                    else:
                        return None
                return magnets
            else:
                return None
        else:
            return None
