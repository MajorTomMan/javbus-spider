import threading
from javbus.utils.attrs_util import AttrsUtil
from javbus.utils.attrs.company_links import CompanyLinks

from javbus.items import ActressItem


class ActressUtil:
    attrsUtil = AttrsUtil()
    lock = threading.Lock()

    def get_details(self, source):
        if source:
            actress = self.getInfo(source)
            if actress:
                return actress
            else:
                return None
        else:
            self.logUtil.log("actress detail page not found")
            return None

    def get_info(self, bs):
        box = bs.find("div", {"class": "avatar-box"})
        if box:
            actress = ActressItem()
            frame = box.find("div", {"class": "photo-frame"})
            info = box.find("div", {"class": "photo-info"})
            if frame:
                link = self.attrsUtil.getPhotoLink(frame)
                actress["photo_link"] = link
            else:
                self.logUtil.log("photo link not found")
            if info:
                name = self.attrsUtil.getName(info)
                if name:
                    actress["name"] = name
                ps = info.find_all("p")
                if ps:
                    for p in ps:
                        if "生日:" in p.text:
                            birth_day = self.attrsUtil.getBirthDay(p)
                            actress["birth_day"] = birth_day
                        if "年齡:" in p.text:
                            age = self.attrsUtil.getAge(p)
                            if age:
                                actress["age"] = age
                        if "罩杯:" in p.text:
                            cup = self.attrsUtil.getCup(p)
                            if cup:
                                actress["cup"] = cup
                        if "身高:" in p.text:
                            height = self.attrsUtil.getHeight(p)
                            if height:
                                actress["height"] = height
                        if "胸圍:" in p.text:
                            bust = self.attrsUtil.getBust(p)
                            if bust:
                                actress["bust"] = bust
                        if "腰圍:" in p.text:
                            waist = self.attrsUtil.getWaist(p)
                            if waist:
                                actress["waist"] = waist
                        if "臀圍:" in p.text:
                            hip = self.attrsUtil.getHip(p)
                            if hip:
                                actress["hip"] = hip
                        if "出生地:" in p.text:
                            brith_place = self.attrsUtil.getBirthPlace(p)
                            if brith_place:
                                actress["birth_place"] = brith_place
                        if "愛好:" in p.text:
                            hobby = self.attrsUtil.getHobby(p)
                            if hobby:
                                actress["hobby"] = hobby
            return actress
        else:
            self.logUtil.log("actress detail page not found")
            return None
