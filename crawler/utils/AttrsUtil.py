from utils.attrs.BanList import Ban


class AttrsUtil:
    ban = Ban()

    def getLink(self, bs):
        a = bs.find("a", {"class": "movie-box"})
        if a:
            link = a["href"]
            return link
        print("link not found")
        return None

    def getTitle(self, bs):
        h3 = bs.find("h3")
        if h3:
            title = h3.text
            return title
        else:
            print("title not found")
            return None

    def getBigImage(self, bs, url):
        if url.endswith("/"):
            url = url[:-1]
        imgs = bs.find("img")
        if imgs:
            img = imgs["src"]
            imgPath = url + img
            return imgPath
        else:
            print("img not found")
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
            print("sampleImage not found")

    def getCode(self, bs):
        span = bs.find("span", {"style": "color:#CC0000;"})
        if span:
            code = span.text.strip()
            return code
        else:
            print("code not found")
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
            print("director not found")
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
            print("studio not found")
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
            print("label not found")
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
                        print("found ban tag in movie")
                        return -1
                    genres[tag] = href
            return genres
        else:
            print("genres not found")
            return None

    def getCategories(self, bs):
        categories = {}
        ass = bs.find_all("a")
        if ass:
            for a in ass:
                tag = a.text.strip()
                if tag in self.ban.tags:
                    continue
                href = a["href"]
                categories[tag] = href
            return categories
        else:
            print("categories not found")
            return None

    def getStars(self, bs):
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
            print("stars not found")
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
            print("series not found")
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
            print("name not found")
            return None

    def getSingleStarLink(self, bs):
        box = bs.find("a", {"class": "avatar-box text-center"})
        if box:
            img = box.find("img")
            if img:
                name = img["title"]
                photo_link = img["src"]
                return {
                    "name": name,
                    "photo_link": photo_link,
                    "star_link": box["href"],
                }
        else:
            print("page stars not found")
            return None
