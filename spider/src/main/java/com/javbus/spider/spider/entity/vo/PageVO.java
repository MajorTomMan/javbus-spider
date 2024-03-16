package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;

@Data
public class PageVO {
    Movie movie;
    Director director;
    List<Actress> actresses;
    Studio studio;
    Series series;
    Label label;
    BigImage bigImage;
    List<Category> categories;
    List<SampleImage> sampleImages;
}
