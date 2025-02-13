

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from javbus.items import (
    ActressCategoryItem,
    ActressDirectorItem,
    ActressesImageItem,
    ActressSeriesItem,
    ActressStudioItem,
    GenreCategoryItem,
    MovieActressItem,
    MovieCategoryItem,
    MovieDirectorItem,
    MovieLabelItem,
    MovieMagnetItem,
    MovieSeriesItem,
    MovieStudioItem,
    PageItem,
)
from javbus.utils.request_util import RequestUtil


class JavbusPipeline:

    def __init__(self) -> None:
        self.request_util = RequestUtil()
        # 定义类型和接口的映射字典
        self.path_map = {
            ActressCategoryItem: "/actress/relation/category/save",
            ActressDirectorItem: "/actress/relation/director/save",
            ActressesImageItem: "/actress/relation/image/save",
            ActressSeriesItem: "/actress/relation/series/save",
            ActressStudioItem: "/actress/relation/studio/save",
            GenreCategoryItem: "/genre/relation/category/save",
            MovieActressItem: "/movie/relation/actress/save",
            MovieCategoryItem: "/movie/relation/category/save",
            MovieDirectorItem: "/movie/relation/director/save",
            MovieLabelItem: "/movie/relation/label/save",
            MovieMagnetItem: "/movie/relation/magnet/save",
            MovieSeriesItem: "/movie/relation/series/save",
            MovieStudioItem: "/movie/relation/studio/save",
        }

    def process_item(self, item, spider):
        item_type = type(item)
        if item_type is PageItem:
            trans_page(item)
        elif item_type in self.path_map:
            # 获取接口 URL
            endpoint = self.path_map[item_type]

            # 使用 ItemAdapter 转换 Item 数据
            item_data = ItemAdapter(item).asdict()

            # 发送数据
            self.request_util.send(item_data, endpoint)

        # 返回处理后的 item
        return item

def trans_page(page):
        movie = page.get("movie")
        label = page.get("label")
        director = page.get("director")
        studio = page.get("studio")
        series = page.get("series")
        actresses = page.get("actresses")
        bigimage = page.get("bigimage")
        categories = page.get("categories")
        sampleimage = page.get("sampleimage")
        magnets = page.get("magnets")
        # 关系 item 填充
        actress_category_item = ActressCategoryItem()
        actress_category_item["actress"] = actresses
        actress_category_item["category"] = categories
        yield actress_category_item

        actress_director_item = ActressDirectorItem()
        actress_director_item["actress"] = actresses
        actress_director_item["director"] = director
        yield actress_director_item

        actresses_image_item = ActressesImageItem()
        actresses_image_item["actress"] = actresses
        actresses_image_item["image"] = bigimage
        yield actresses_image_item

        actress_series_item = ActressSeriesItem()
        actress_series_item["actress"] = actresses
        actress_series_item["series"] = series
        yield actress_series_item

        actress_studio_item = ActressStudioItem()
        actress_studio_item["actress"] = actresses
        actress_studio_item["studio"] = studio
        yield actress_studio_item

        movie_actress_item = MovieActressItem()
        movie_actress_item["movie"] = movie
        movie_actress_item["actress"] = actresses
        yield movie_actress_item

        movie_category_item = MovieCategoryItem()
        movie_category_item["movie"] = movie
        movie_category_item["categories"] = categories
        yield movie_category_item

        movie_director_item = MovieDirectorItem()
        movie_director_item["movie"] = movie
        movie_director_item["director"] = director
        yield movie_director_item

        movie_label_item = MovieLabelItem()
        movie_label_item["movie"] = movie
        movie_label_item["label"] = label
        yield movie_label_item

        movie_magnet_item = MovieMagnetItem()
        movie_magnet_item["movie"] = movie
        movie_magnet_item["magnets"] = magnets
        yield movie_magnet_item

        movie_series_item = MovieSeriesItem()
        movie_series_item["movie"] = movie
        movie_series_item["series"] = series
        yield movie_series_item

        movie_studio_item = MovieStudioItem()
        movie_studio_item["movie"] = movie
        movie_studio_item["studio"] = studio
        yield movie_studio_item
