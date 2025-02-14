# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from javbus.items import (
    ActressesItem,
    GenreCategoryItem,
    MovieActressItem,
    MovieCategoryItem,
    MovieDirectorItem,
    MovieLabelItem,
    MovieMagnetItem,
    MovieSeriesItem,
    MovieStudioItem,
    MovieBigImageItem,
    MovieSampleItem,
    PageItem,
)
from javbus.utils.request_util import RequestUtil


class JavbusPipeline:

    def __init__(self) -> None:
        self.request_util = RequestUtil()
        # 定义类型和接口的映射字典
        self.path_map = {
            ActressesItem: "/actress/save",
            GenreCategoryItem: "/genre/relation/category/save",
            MovieActressItem: "/movie/relation/actress/save",
            MovieCategoryItem: "/movie/relation/category/save",
            MovieDirectorItem: "/movie/relation/director/save",
            MovieLabelItem: "/movie/relation/label/save",
            MovieMagnetItem: "/movie/relation/magnet/save",
            MovieSeriesItem: "/movie/relation/series/save",
            MovieStudioItem: "/movie/relation/studio/save",
            MovieBigImageItem: "/movie/relation/bigimage/save",
            MovieSampleItem: "/movie/relation/sampleimage/save",
        }

    def process_item(self, item, spider):
        item_type = type(item)
        if item_type is PageItem:
            self.trans_page(item)
        elif item_type in self.path_map:
            # 获取接口 URL
            endpoint = self.path_map[item_type]

            # 使用 ItemAdapter 转换 Item 数据
            item_data = ItemAdapter(item).asdict()

            # 发送数据
            self.request_util.send(item_data, endpoint)

        # 返回处理后的 item
        return item

    def trans_page(self, page):
        movie = page.get("movie")
        label = page.get("label")
        director = page.get("director")
        studio = page.get("studio")
        series = page.get("series")
        categories = page.get("categories")
        magnets = page.get("magnets")
        actresses = page.get("actresses")
        bigimage = page.get("bigimage")
        sampleimages = page.get("sampleimages")
        if movie:
            if actresses:
                movie_actress_item = MovieActressItem(movie=movie, actress=actresses)
                self.request_util.send(
                    ItemAdapter(movie_actress_item).asdict(),
                    self.path_map[MovieActressItem],
                )
            if categories:
                movie_category_item = MovieCategoryItem(
                    movie=movie, categories=categories
                )
                self.request_util.send(
                    ItemAdapter(movie_category_item).asdict(),
                    self.path_map[MovieCategoryItem],
                )
            if director:
                movie_director_item = MovieDirectorItem(movie=movie, director=director)
                self.request_util.send(
                    ItemAdapter(movie_director_item).asdict(),
                    self.path_map[MovieDirectorItem],
                )
            if label:
                movie_label_item = MovieLabelItem(movie=movie, label=label)
                self.request_util.send(
                    ItemAdapter(movie_label_item).asdict(),
                    self.path_map[MovieLabelItem],
                )
            if magnets:
                movie_magnet_item = MovieMagnetItem(movie=movie, magnets=magnets)
                self.request_util.send(
                    ItemAdapter(movie_magnet_item).asdict(),
                    self.path_map[MovieMagnetItem],
                )
            if series:
                movie_series_item = MovieSeriesItem(movie=movie, series=series)
                self.request_util.send(
                    ItemAdapter(movie_series_item).asdict(),
                    self.path_map[MovieSeriesItem],
                )
            if studio:
                movie_studio_item = MovieStudioItem(movie=movie, studio=studio)
                self.request_util.send(
                    ItemAdapter(movie_studio_item).asdict(),
                    self.path_map[MovieStudioItem],
                )
            if bigimage:
                movie_bigimage_item = MovieBigImageItem(movie=movie, big_image=bigimage)
                self.request_util.send(
                    ItemAdapter(movie_bigimage_item).asdict(),
                    self.path_map[MovieBigImageItem],
                )
            if sampleimages:
                movie_sampleimages_item = MovieSampleItem(
                    movie=movie, sample_images=sampleimages
                )
                self.request_util.send(
                    ItemAdapter(movie_sampleimages_item).asdict(),
                    self.path_map[MovieSampleItem],
                )
