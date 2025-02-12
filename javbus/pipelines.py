# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from javbus.items import (
    MovieItem,
    ActressItem,
    BigImageItem,
    CategoryItem,
    DirectorItem,
    LabelItem,
    MagnetItem,
    GenresItem,
)
from javbus.utils.request_util import RequestUtil


class JavbusPipeline:
    def __init__(self) -> None:
        self.request_util = RequestUtil()
        # 定义类型和接口的映射字典
        self.path_map = {
            GenresItem: "/genre/relation/category/save",
            ActressItem: "/actress/save",
            MovieItem: "/movie/save",
            BigImageItem: "/movie/relation/bigimage/save",
            CategoryItem: "/movie/relation/category/save",
            DirectorItem: "/movie/relation/director/save",
            LabelItem: "/movie/relation/label/save",
            MagnetItem: "/movie/relation/magnet/save",
        }

    def process_item(self, item, spider):
        item_type = type(item)

        if item_type in self.path_map:
            # 获取接口 URL
            endpoint = self.path_map[item_type]

            # 使用 ItemAdapter 转换 Item 数据
            item_data = ItemAdapter(item).asdict()

            # 发送数据
            self.request_util.send(item_data, endpoint)

        # 返回处理后的 item
        return item
