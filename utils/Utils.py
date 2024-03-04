import warnings
import os
import requests


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebUtil:
    def __init__(self) -> None:
        self.options=Options()
        self.ua=UserAgent()
        self.__configure()

    def __configure(self):
        # selenium configuration for headless browser mode
        warnings.simplefilter("ignore", ResourceWarning)
        #WebUtils.options.add_argument("--headless")
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
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'useAutomationExtension','enable-logging'])
    

    def getWebSite(self,url):
        user_agent = self.ua.random
        driver = webdriver.Chrome(options=self.options)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
        driver.get(url)
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

    def getName(self, bs):
        names={}
        a = bs.find("a")
        if a:
            href = a["href"]
            name = a.text
            names[name] = href
            return names
        else:
            print("name not found")
            return None

    def getSeries(self, bs):
        series={}
        a = bs.find("a")
        if a:
            href = a["href"]
            serie = a.text
            series[serie] = href
            return serie
        else:
            print("series not found")
            return None
        
        
class ImageUtil:
    def __init__(self) -> None:
        self.ua=UserAgent()
        self.basePath="./images/"
    def downloadSampleImages(self,links,attrs):
        headers={"User-Agent":self.ua.random}
        for link in links:
            filename=link.split("/")[-1]
            if self.__checkFileIsExists(attrs=attrs,filename=filename,isBigImage=False):
                print("local sample file "+filename+" already exists skipping download")
                continue
            response=requests.get(link,headers=headers)
            print("image response code is "+str(response.status_code))
            if response.status_code==200:
                print("image "+ response.url+" download success")
                self.__save2Local(response,attrs,filename,False)
            else:
                print("image "+ response.url+" download failure")
    def downloadBigImage(self,link,attrs):
        filename=link.split("/")[-1]
        if self.__checkFileIsExists(attrs=attrs,filename=filename,isBigImage=True):
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
            self.__save2Local(response,attrs,filename,True)
        else:
            print("image "+ response.url+" download failure")
        
    def __save2Local(self,response,attrs,filename,isBigImage):
        if not isBigImage:
            targetFolder=self.basePath+attrs.name+"/"+attrs.code+"/"+"sample"+"/"
        else:
            targetFolder=self.basePath+attrs.name+"/"+attrs.code+"/"+"bigImage"+"/"
        path=targetFolder+filename
        print("current image store path is "+path)
        if self.__checkFolderIsExists(targetFolder):
            self.__save(response,path)
        else:
            os.makedirs(targetFolder)
            self.__save(response,path)
        print("image "+path+" is downloaded")
        
    def __checkFolderIsExists(self,path):
        if os.path.exists(path):
            print(path+" exists")
            return True
        print(path+" not exists")
        return False
    def __checkFileIsExists(self,attrs,filename,isBigImage):
        if isBigImage:
            path=self.basePath+attrs.name+"/"+attrs.code+"/"+"sample"+"/"+filename
        else:
            path=self.basePath+attrs.name+"/"+attrs.code+"/"+"bigImage"+"/"+filename
        if os.path.exists(path):
            return True
        return False
    def __save(self,response,path):
        with open(path,"wb") as f:
            for cache in response.iter_content(chunk_size=32):
                f.write(cache)