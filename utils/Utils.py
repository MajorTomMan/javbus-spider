import json
import time
import warnings
import os
from bs4 import BeautifulSoup
import requests

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By


from utils.attrs.Director import Director
from utils.attrs.Movie import Movie
from utils.attrs.Star import Star
from utils.attrs.Studio import Studio
from utils.attrs.Series import Series
from utils.attrs.Category import Category
from utils.attrs.Label import Label


class WebUtil:
    def __init__(self) -> None:
        self.options=Options()
        self.ua=UserAgent()
        self.__configure()

    def __configure(self):
        # selenium configuration for headless browser mode
        warnings.simplefilter("ignore", ResourceWarning)
        self.options.add_argument("--headless")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--disable-web-security')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--user-data-dir=/dev/null')
        self.options.add_argument('--remote-debugging-port=12000')
        #self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'useAutomationExtension','enable-logging'])

    def getWebSite(self,url):
        driver = uc.Chrome(headless=True)
        driver.get(url)
        time.sleep(6)
        return driver
    def save2local(self,path,filename,content):
        with open(path+"/"+filename+".html", "w", encoding="utf-8") as f:
            f.write(content)
        
    def checkisLimitedByAge(self, content):
        if "Age" in content:
            return True
        elif "Verification" in content:
            return True
        else:
            return False

    def usingSeleniumToFix(self, driver):
        checkbox = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/form/div/label/input")
        if checkbox:
            checkbox.click()
            submit = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/form/input")
            if submit:
                submit.click()
        else:
            print("checkbox not found")

    def get(self,url):
        headers={
            "User-Agent": self.ua.random
        }
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        else:
            return None
class AttrsUtil:
    def getLink(self, bs):
        a = bs.find("a", {"class": "movie-box"})
        if a:
            link = a["href"]
            return link
        else:
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

    def getBigImage(self, bs,url):
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
        director={}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text.strip()
            director[name]=href
            return director
        else:
            print("director not found")
            return None

    def getStudio(self, bs):
        studio={}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text.strip()
            studio[name]=href
            return studio
        else:
            print("studio not found")
            return None

    def getLabel(self, bs):
        labels={}
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
        genres={}
        genresList = bs.find_all("span", {"class": "genre"})
        if genresList:
            for genre in genresList:
                a = genre.find("a")
                if a:
                    href = a["href"]
                    g = a.text.strip()
                    genres[g]=href
            return genres
        else:
            print("genres not found")
            return None

    def getStars(self, bs):
        names={}
        spans=bs.find_all("span",{"class":"genre"})
        if spans:
            for span in spans:
                a=span.find("a")
                if a:
                    link=a["href"]
                    name=a.text
                    names[name]=link
            return names
        else:
            print("stars not found")
            return None

    def getSeries(self, bs):
        series={}
        a = bs.find("a")
        if a:
            href = a["href"]
            serie = a.text
            series[serie] = href
            return series
        else:
            print("series not found")
            return None
    def getPhotoLink(self,bs):
        img=bs.find("img")
        if img:
            src=img["src"]
            return src
    def getBrithDay(self,bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getAge(self,bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getHeight(self,bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getCup(self,bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getBust(self,bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getWaist(self, bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getHip(self, bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getBirthPlace(self, bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()

    def getHobby(self, bs):
        attr=bs.text.split(":")
        if attr:
            return attr[-1].strip()
    def getName(self,bs):
        span=bs.find("span",{"class":"pb10"})
        if span:
            name=span.text
            return name.strip()
        else:
            print("name not found")
            return None
class ImageUtil:
    def __init__(self) -> None:
        self.ua=UserAgent()
        self.basePath="./images/"
    def downloadSampleImages(self,links,movie):
        if movie.stars==None:
            stars="演员未知"
        elif len(movie.stars)>1:
            stars="-".join(movie.stars.keys())
        elif len(movie.stars)==1:
            stars=list(movie.stars.keys())[0]
        else:
            return
        headers={"User-Agent":self.ua.random}
        for link in links:
            filename=link.split("/")[-1]
            if self.__checkFileIsExists(stars=stars,code=movie.code,filename=filename,isBigImage=False):
                print("local sample file "+filename+" already exists skipping download")
                continue
            response=requests.get(link,headers=headers)
            print("image response code is "+str(response.status_code))
            if response.status_code==200:
                print("image "+ response.url+" download success")
                self.__save2Local(response=response,stars=stars,code=movie.code,filename=filename,isBigImage=False)
            else:
                print("image "+ response.url+" download failure")
    def downloadBigImage(self,link,movie):
        if movie.stars==None:
            stars="演员未知"
        elif len(movie.stars)>1:
            stars="-".join(movie.stars.keys())
        elif len(movie.stars)==1:
            stars=list(movie.stars.keys())[0]
        else:
            return
        filename=link.split("/")[-1]
        if self.__checkFileIsExists(stars=stars,code=movie.code,filename=filename,isBigImage=True):
            print("local bigImage file "+filename+" already exists skipping download")
            return
        headers={"User-Agent":self.ua.random}
        response=requests.get(link,headers=headers)
        print("image response code is "+str(response.status_code))
        print("image response url is "+response.url)
        if response.status_code==200:
            print("image "+ response.url+" download success")
            url=response.url
            paths=url.split("/")
            filename=paths[-1]
            self.__save2Local(response=response,stars=stars,code=movie.code,filename=filename,isBigImage=True)
        else:
            print("image "+ response.url+" download failure")
        
    def __save2Local(self,response,stars,code,filename,isBigImage):
        if not isBigImage:
            targetFolder=self.basePath+stars+"/"+code+"/"+"sample"+"/"
        else:
            targetFolder=self.basePath+stars+"/"+code+"/"+"bigImage"+"/"
        path=targetFolder+filename
        print("current image store path is "+path)
        if self.__checkFolderIsExists(targetFolder):
            self.__save(response,path)
        else:
            print("create folder "+targetFolder)
            os.makedirs(targetFolder)
            self.__save(response,path)
        print("image "+path+" is downloaded")
        
    def __checkFolderIsExists(self,path):
        if os.path.exists(path):
            print(path+" exists")
            return True
        print(path+" not exists")
        return False
    def __checkFileIsExists(self,stars,code,filename,isBigImage):
        if not isBigImage:
            path=self.basePath+stars+"/"+code+"/"+"sample"+"/"+filename
        else:
            path=self.basePath+stars+"/"+code+"/"+"bigImage"+"/"+filename
        if os.path.exists(path):
            return True
        return False
    def __save(self,response,path):
        with open(path,"wb") as f:
            for cache in response.iter_content(chunk_size=32):
                f.write(cache)
                
                
class PageUtil:
    WebUtil=WebUtil()
    AttrsUtil=AttrsUtil()
    ImageUtil=ImageUtil()
    baseUrl=""
    def __init__(self,url) -> None:
        self.baseUrl=url
    def parseDetailPage(self, link):
        driver = self.WebUtil.getWebSite(link)
        bs = BeautifulSoup(driver.page_source,"html.parser")
        title = self.AttrsUtil.getTitle(bs)
        movie = self.getInfos(bs)
        movie.title=title
        a = bs.find("a", {"class": "bigImage"})
        if a:
            bigImagePath=self.AttrsUtil.getBigImage(a,self.baseUrl)
            movie.big_image_link=bigImagePath
        waterfall = bs.find("div", {"id": "sample-waterfall"})
        if waterfall:
            imgs = self.AttrsUtil.getSampleImages(waterfall)
            if imgs:
                if movie:
                    movie.sample_image_links=imgs
        self.ImageUtil.downloadSampleImages(links=movie.sample_image_links,movie=movie)
        self.ImageUtil.downloadBigImage(link=movie.big_image_link,movie=movie)
        return movie
    def getInfos(self, bs):
        movie=Movie()
        director=Director()
        series=Series()
        studio=Studio()
        label=Label()
        info = bs.find("div", {"class": "col-md-3 info"})
        if info:
            ps = info.find_all("p")
            for p in ps:
                header = p.find("span", {"class": "header"})
                if header:
                    if "識別碼:" in header:
                        code = self.AttrsUtil.getCode(p)
                        movie.code=code
                    if "發行日期:" in header:
                        date = self.AttrsUtil.getReleaseDate(header)
                        movie.release_date=date
                    if "長度:" in header:
                        length = self.AttrsUtil.getLength(header)
                        movie.length=length
                    if "導演:" in header:
                        d = self.AttrsUtil.getDirector(p)
                        director.name=list(d.keys())[0]
                        director.link=d.get(director.name)
                        movie.director=director.toDict()
                    if "製作商:" in header:
                        s = self.AttrsUtil.getStudio(p)
                        studio.name=list(s.keys())[0]
                        studio.link=s.get(studio.name)
                        movie.studio=studio.toDict()
                    if "發行商:" in header:
                        l = self.AttrsUtil.getLabel(p)
                        label.name=list(l.keys())[0]
                        label.link=l.get(label.name)
                        movie.label=label.toDict()
                    if "系列:" in header:
                        s = self.AttrsUtil.getSeries(p)
                        if s:
                            series.name=list(s.keys())[0]
                            series.link=s.get(series.name)
                            movie.series=series.toDict()
                        else:
                            print("series not found")
            p = ps[-1]
            stars = self.AttrsUtil.getStars(p)
            movie.stars=stars
            p=ps[-3]
            genres = self.AttrsUtil.getGenres(p)
            if genres:
                movie.categories=genres
            else:
                print("genres not found")
            return movie
        else:
            print("info not found")
            return None
    def parseStarDetailsPage(self,link):
        driver=self.WebUtil.getWebSite(link)
        bs=BeautifulSoup(driver.page_source,"html.parser")
        star=Star()
        box=bs.find("div",{"class":"avatar-box"})
        if box:
            frame=box.find("div",{"class":"photo-frame"})
            info=box.find("div",{"class":"photo-info"})
            if frame:
                link=self.AttrsUtil.getPhotoLink(frame)
                if self.baseUrl.endswith("/"):
                    url = self.baseUrl[:-1]
                    star_link=url+link
                    star.photo_link=star_link
            else:
                print("photo link not found")
            if info:
                name=self.AttrsUtil.getName(info)
                if name:
                    star.name=name
                ps=info.find_all("p")
                if ps:
                    for p in ps:
                        if "生日:" in p.text:
                             brithday=self.AttrsUtil.getBrithDay(p)
                             star.brith_day=brithday
                        if "年齡:" in p.text:
                            age=self.AttrsUtil.getAge(p)
                            if age:
                                star.age=age
                        if "罩杯:" in p.text:
                            cup=self.AttrsUtil.getCup(p)
                            if cup:
                                star.cup=cup
                        if "身高:" in p.text:
                            height=self.AttrsUtil.getHeight(p)
                            if height:
                                star.height=height
                        if "胸圍:" in p.text:
                            bust=self.AttrsUtil.getBust(p)
                            if bust:
                                star.bust=bust
                        if "腰圍:" in p.text:
                            waist=self.AttrsUtil.getWaist(p)
                            if waist:
                                star.waist=waist
                        if "臀圍:" in p.text:
                            hip=self.AttrsUtil.getHip(p)
                            if hip:
                                star.hip=hip
                        if "出生地:" in p.text:
                            brith_place=self.AttrsUtil.getBirthPlace(p)
                            if brith_place:
                                star.birth_place=brith_place
                        if "愛好:" in p.text:
                            hobby=self.AttrsUtil.getHobby(p)
                            if hobby:
                                star.hobby=hobby
        else:
            print("star detail page not found")
        return star
class RequestUtil:
    baseUrl="http://localhost:8080"
    headers={'Content-Type': 'application/json'}
    def post(self,data,path):
        return requests.post(url=self.baseUrl+path,json=data)
    def get(self,path):
        return requests.get(self.baseUrl+path)


