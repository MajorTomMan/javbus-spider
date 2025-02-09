import scrapy
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from javbus.items import CategoryItem
from scrapy_redis.spiders import RedisSpider

class GenreSpider(RedisSpider):
    name = "genre"
    base_url = ""

    def __init__(self, url, is_censored=True, *args, **kwargs):
        super(GenreSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.is_censored = is_censored

    def parse(self, response):
        source = response.text
        bs = BeautifulSoup(source, "html.parser")

        # 提取所有的 genres 和 boxs
        genres = self.extract_genres(bs)
        boxs = self.extract_boxes(bs)

        # 定义一个数组来保存所有的 vos
        all_vos = []

        if genres and boxs:
            # 遍历并提取每个 box 相关的数据
            for index, box in enumerate(boxs):
                categories = self.get_categories(box)
                if categories:
                    vos = self.build_vos(genres, index, categories)
                    if vos:
                        all_vos.extend(vos)  # 将 vos 添加到 all_vos 中
        else:
            # 如果没有数据，可以选择保存原始页面内容或进行其他处理
            self.save_to_local(source, response.url)

        # 在所有数据处理完之后统一 yield
        if all_vos:
            for vo in all_vos:
                yield vo

    def extract_genres(self, bs):
        """提取所有的 genres（如果有）"""
        genres = []
        titles = bs.find_all("h4", {"class": "modal-title"})
        for title in titles:
            title.extract()  # 移除标题内容

        # 找到所有 h4 标签并提取
        h4s = bs.find_all("h4")
        for h4 in h4s:
            genres.append(h4.text.strip())
        return genres

    def extract_boxes(self, bs):
        """提取所有的 genre-boxes（如果有）"""
        return bs.find_all("div", {"class": "row genre-box"})

    def get_categories(self, box):
        """从每个 box 中提取类别链接"""
        categories = {}
        links = box.find_all("a", href=True)
        for link in links:
            category_name = link.text.strip()
            category_link = link["href"]
            categories[category_name] = category_link
        return categories

    def build_vos(self, genres, index, categories):
        """根据 genre 和 category 构建 vos 数据"""
        if index < len(genres):  # 确保 index 不超出 genres 列表的范围
            key = genres[index]
            vos = {
                "genre": {"name": key},
                "categories": [
                    {"name": k, "link": v, "is_censored": self.is_censored} 
                    for k, v in categories.items()
                ]
            }
            return vos

        return None

    def save_to_local(self, content, link):
        """保存内容到本地文件"""
        parsed_url = urlparse(link)
        path_name = parsed_url.path.replace("/", "_")
        hash_value = hashlib.md5(path_name.encode()).hexdigest()
        save_path = f"./failed_link/{path_name}_{hash_value}.html"

        with open(save_path, "w+", encoding="UTF-8") as f:
            f.write(content)
