import requests
import json
from bs4 import BeautifulSoup

url = "http://192.168.253.131:8191/v1"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5",
    "Cache-Control": "no-cache",
    "Cookie": "timezone=-480; dm=javlibrary; UGVyc2lzdFN0b3JhZ2U=%7B%7D; over18=18; __PPU_tuid=7471246596718840062; __PPU_ppucnt=3; cf_clearance=zz.7UkKygWM9UHXvhzvwAK1BdINEd5oSx2d0HhALvEM-1739536924-1.2.1.1-hxo0DDOj3vNBi5EoIFxgKL7eQO1YqkP0cRK_kSUwPPg8C.z69MduGQSZVizOZ1g0VKRo.rWFLDNC.JIFz.MCp83Yp9XXi8Tf0O5skKpfrZTnOTRPYtO9iVEfVuCYgZrp5fWhNqajBQgAqN0lsra392GH93BwlQR5jAqd86AAG2frdr.MWRlI6s5edzsZKGJUADee73JZEDftCKR5Hp5iR8qHEEHYiUT9F0WEhS6W2.kPI793Db.icH0vRTWoAjybBuFhm7g_wHPnvD9P_GkNq1FfXyIJ198d57k9hl0e5HO4lgMdhBir9Ax9INt6ZchCDIs81OAMPKzGtYqGkJmezg",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Referer": "https://www.javlibrary.com/cn/?v=javmefb6ri",
    "Sec-CH-UA": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "Sec-CH-UA-Arch": '"x86"',
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Full-Version": '"132.0.6834.197"',
    "Sec-CH-UA-Full-Version-List": '"Not A(Brand";v="8.0.0.0", "Chromium";v="132.0.6834.197", "Google Chrome";v="132.0.6834.197"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Model": '""',
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-CH-UA-Platform-Version": '"10.0.0"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
}

data = {
    "cmd": "request.post",
    "url": "https://www.javlibrary.com/cn/vl_searchbyid.php",
    "postData": "?keyword=MUCH-187",
    "maxTimeout": 60000,
    "proxy": {"url":"http://192.168.253.1:10809"},
    "headers": headers
}
response = requests.post(url, headers=headers, json=data)
response = json.loads(response.content)
source = response["solution"]["response"]
bs = BeautifulSoup(source, "html.parser")
print(bs)
