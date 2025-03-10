'''
Date: 2025-02-19 21:37:06
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-01 19:46:11
FilePath: \spiders\spider\javbus\spiders\ip_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''

from re import L
import scrapy
import json
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
from javbus.common.constants import get_cloud_ip_proxy_url
from javbus.common.redis_keys import proxy_ip_key
from spider.base.base_spider import BaseSpider

class IP_Proxy_Spider(BaseSpider):
    name = "ip_proxy"

    def start_requests(self):
        yield scrapy.Request(url=get_cloud_ip_proxy_url,callback=self.parse,dont_filter=True,headers={})

    # 用于解析reponse的方法
    def parse(self, response):
            if response.status == 200:
                # 使用 BeautifulSoup 解析 HTML
                soup = BeautifulSoup(response.text, "html.parser")   

                # 获取纯文本内容，并按换行符拆分
                text_content = soup.get_text(separator="\n")

                # 按换行符拆分并去掉空白项
                ip_list = [ip.strip() for ip in text_content.split("\n") if ip.strip() and ':' in ip]
                if len(ip_list)>1:
                    # 输出结果
                    ip_list = ip_list[:-1]
                    for ip in ip_list:
                        ip = ip.split(":")
                        ip_dict = {"ip":ip[0],"port":ip[1]}
                        self.server.sadd(proxy_ip_key,json.dumps(ip_dict))