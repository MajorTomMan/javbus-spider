'''
Date: 2025-03-10 21:19:15
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-03-16 17:52:55
FilePath: \spider\javbus\spiders\movie_spider.py
Description: MajorTomMan @版权声明 保留文件所有权利
'''

import json
from javbus.utils.page_util import PageUtil
from bs4 import BeautifulSoup
from javbus.common.redis_keys import actress_detail_start_url_key
from base.base_spider import BaseSpider

class MovieSpider(BaseSpider):
    name = "movie"
    allowed_domains = None

    def parse(self, response):
        if response.status == 200:
            link = response.url
            is_censored = response.meta["is_censored"]
            bs = BeautifulSoup(response.body, "html.parser")
            page = PageUtil().parse_page(
                link=link,
                source=bs,
                is_censored=is_censored,
            )
            if page == -1 or page is None:
                self.log("in " + link + " found ban tag skipping crawl")
                return
            actresses = page["actresses"]
            # 启动女优详情页爬虫
            if actresses:
                for actress in actresses:
                    actress["is_censored"] = is_censored
                    actress_link = actress["actress_link"]
                    if actress_link:
                        actress_detail_request_data = {
                            "url": actress_link,
                            "meta":{
                                "is_censored": is_censored
                            }
                        }
                        self.push_to_redis(
                            actress_detail_start_url_key,
                            json.dumps(actress_detail_request_data),
                        )
            else:
                self.log("get actresses failed")
            yield page
        else:
            self.log("Request failed with status code: {}".format(response.status))
