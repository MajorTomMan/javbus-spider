import requests
from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

class SearchPageUtil:
    def get_topic_image(self,response,cookies):
        if response:
            bs = BeautifulSoup(response.content,"html.parser")
            topic = bs.find("div", {"class": "Po_topic"})
            if topic:
                link = topic.find("a")["href"]
                if link:
                    response = requests.get(link, headers=headers, cookies=cookies)
                    if response.status_code == 200:
                        bs = BeautifulSoup(response.content, "html.parser")
                        info = bs.find("div", id="info")
                        if info:
                            info_cg = info.find("div",{"class":"info_cg"})
                            if info_cg:
                                src = info_cg.find("img")["src"]
                                if src:
                                    return src
                                else:
                                    return None
                            else:
                                return None
                        else:
                            return None
            else:
                return None
