import requests

cookies = {
    'PHPSESSID': 'k31jhiep16k77or3hv2t653sd6',
    'existmag': 'mag',
}

headers = {
    'authority': 'www.javbus.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'PHPSESSID=k31jhiep16k77or3hv2t653sd6; existmag=mag',
    'referer': 'https://www.javbus.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'floor': '950',
    'lang': 'zh',
}

response = requests.get('https://www.javbus.com/ajax/search-modal.php', params=params, cookies=cookies, headers=headers)
print(response.text)