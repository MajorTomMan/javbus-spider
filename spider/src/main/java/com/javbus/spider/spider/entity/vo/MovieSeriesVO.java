package com.javbus.spider.spider.entity.vo;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Series;

import lombok.Data;

@Data
public class MovieSeriesVO {
    Movie movie;
    Series series;
}
