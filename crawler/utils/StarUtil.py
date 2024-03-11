import time
from bs4 import BeautifulSoup
from utils.AttrsUtil import AttrsUtil
from utils.LogUtil import LogUtil
from utils.WebUtil import WebUtil

from utils.attrs.Star import Star


class StarUtil:
    webUtil = WebUtil()
    attrsUtil = AttrsUtil()
    logUtil = LogUtil()

    def getStarDetails(self, link):
        self.logUtil.log("sleeping in 10 seconds")
        time.sleep(5)
        source = self.webUtil.getWebSite(link)
        if source:
            bs = BeautifulSoup(source, "html.parser")
            star = Star()
            box = bs.find("div", {"class": "avatar-box"})
            if box:
                frame = box.find("div", {"class": "photo-frame"})
                info = box.find("div", {"class": "photo-info"})
                if frame:
                    link = self.attrsUtil.getPhotoLink(frame)
                    star.photo_link = link
                else:
                    self.logUtil.log("photo link not found")
                if info:
                    name = self.attrsUtil.getName(info)
                    if name:
                        star.name = name
                    ps = info.find_all("p")
                    if ps:
                        for p in ps:
                            if "生日:" in p.text:
                                birthday = self.attrsUtil.getBirthDay(p)
                                star.brith_day = birthday
                            if "年齡:" in p.text:
                                age = self.attrsUtil.getAge(p)
                                if age:
                                    star.age = age
                            if "罩杯:" in p.text:
                                cup = self.attrsUtil.getCup(p)
                                if cup:
                                    star.cup = cup
                            if "身高:" in p.text:
                                height = self.attrsUtil.getHeight(p)
                                if height:
                                    star.height = height
                            if "胸圍:" in p.text:
                                bust = self.attrsUtil.getBust(p)
                                if bust:
                                    star.bust = bust
                            if "腰圍:" in p.text:
                                waist = self.attrsUtil.getWaist(p)
                                if waist:
                                    star.waist = waist
                            if "臀圍:" in p.text:
                                hip = self.attrsUtil.getHip(p)
                                if hip:
                                    star.hip = hip
                            if "出生地:" in p.text:
                                brith_place = self.attrsUtil.getBirthPlace(p)
                                if brith_place:
                                    star.birth_place = brith_place
                            if "愛好:" in p.text:
                                hobby = self.attrsUtil.getHobby(p)
                                if hobby:
                                    star.hobby = hobby
                return star
            else:
                self.logUtil.log("star detail page not found")
                return None
        else:
            self.logUtil.log("star request " + link + " timeout")
            return None
