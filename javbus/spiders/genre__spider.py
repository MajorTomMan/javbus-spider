import scrapy
import hashlib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.attrs.Category import Category


class GenreSpider(scrapy.Spider):
    name = "genre_spider"

    def __init__(self, url, is_censored=True, *args, **kwargs):
        super(GenreSpider, self).__init__(*args, **kwargs)
        if is_censored:
            self.start_urls = [f"{url}genre/"]
        else:
            self.start_urls = [f"{url}uncensored/genre"]

        self.is_censored = is_censored

    def parse(self, response):
        source = response.text
        bs = BeautifulSoup(source, "html.parser")
        genres = []
        titles = bs.find_all("h4", {"class": "modal-title"})
        for title in titles:
            title.extract()

        h4s = bs.find_all("h4")
        for h4 in h4s:
            genres.append(h4.text.strip())

        if h4s:
            boxs = bs.find_all("div", {"class": "row genre-box"})
            if boxs:
                for index, box in enumerate(boxs):
                    cs = self.get_categories(box)
                    categories = []
                    for k, v in cs.items():
                        category = Category()
                        category.name = k
                        category.link = v
                        category.is_censored = self.is_censored
                        categories.append(category.toDict())

                    key = genres[index]
                    vos = {
                        "genre": {"name": key},
                        "categories": categories,
                    }

                    if vos and len(vos) >= 1:
                        yield self.save_to_server(vos)
            else:
                self.save_to_local(source, response.url)
        else:
            self.save_to_local(source, response.url)

    def get_categories(self, box):
        categories = {}
        links = box.find_all("a", href=True)
        for link in links:
            category_name = link.text.strip()
            category_link = link["href"]
            categories[category_name] = category_link
        return categories

    def save_to_server(self, vos):
        return vos

    def save_to_local(self, content, link):
        parsed_url = urlparse(link)
        path_name = parsed_url.path.replace("/", "_")
        hash_value = hashlib.md5(path_name.encode()).hexdigest()
        save_path = f"./failed_link/{path_name}_{hash_value}.html"

        with open(save_path, "w+", encoding="UTF-8") as f:
            f.write(content)
