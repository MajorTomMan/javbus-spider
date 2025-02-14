"""
Date: 2025-02-07 22:00:29
LastEditors: MajorTomMan 765719516@qq.com
LastEditTime: 2025-02-12 21:17:26
FilePath: \spider\javbus\items.py
Description: MajorTomMan @版权声明 保留文件所有权利
"""

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    code = scrapy.Field()
    link = scrapy.Field()
    release_date = scrapy.Field()
    length = scrapy.Field()
    is_censored = scrapy.Field()


class ActressesItem(scrapy.Item):
    actresses = scrapy.Field()


class ActressItem(scrapy.Item):
    name = scrapy.Field()
    actress_link = scrapy.Field()
    photo_link = scrapy.Field()
    birth_day = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    cup = scrapy.Field()
    bust = scrapy.Field()
    waist = scrapy.Field()
    hip = scrapy.Field()
    birth_place = scrapy.Field()
    hobby = scrapy.Field()
    is_censored = scrapy.Field()


class BigImageItem(scrapy.Item):
    link = scrapy.Field()


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    is_censored = scrapy.Field()


class DirectorItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class ImageItem(scrapy.Item):
    actresses = scrapy.Field()
    images = scrapy.Field()
    names = scrapy.Field()
    code = scrapy.Field()


class LabelItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class MagnetItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    size = scrapy.Field()
    share_date = scrapy.Field()


class PageItem(scrapy.Item):
    movie = scrapy.Field()
    label = scrapy.Field()
    director = scrapy.Field()
    studio = scrapy.Field()
    series = scrapy.Field()
    actresses = scrapy.Field()
    bigimage = scrapy.Field()
    categories = scrapy.Field()
    sampleimages = scrapy.Field()
    magnets = scrapy.Field()


class SampleImageItem(scrapy.Item):
    link = scrapy.Field()


class SeriesItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class GenresItem(scrapy.Item):
    genre = scrapy.Field()
    categories = scrapy.Field()


class GenreItem(scrapy.Item):
    name = scrapy.Field()


class StudioItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class GenreCategoryItem(scrapy.Item):
    genre = scrapy.Field()
    categories = scrapy.Field()


class MovieBigImageItem(scrapy.Item):
    movie = scrapy.Field()
    big_image = scrapy.Field()

class MovieSampleItem(scrapy.Item):
    movie = scrapy.Field()
    sample_images = scrapy.Field()


class MovieActressItem(scrapy.Item):
    movie = scrapy.Field()
    actress = scrapy.Field()


class MovieCategoryItem(scrapy.Item):
    movie = scrapy.Field()
    categories = scrapy.Field()


class MovieDirectorItem(scrapy.Item):
    movie = scrapy.Field()
    director = scrapy.Field()


class MovieLabelItem(scrapy.Item):
    movie = scrapy.Field()
    label = scrapy.Field()


class MovieMagnetItem(scrapy.Item):
    movie = scrapy.Field()
    magnets = scrapy.Field()


class MovieSeriesItem(scrapy.Item):
    movie = scrapy.Field()
    series = scrapy.Field()


class MovieStudioItem(scrapy.Item):
    movie = scrapy.Field()
    studio = scrapy.Field()
