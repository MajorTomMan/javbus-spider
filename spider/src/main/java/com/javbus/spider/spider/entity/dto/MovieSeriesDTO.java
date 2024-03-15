package com.javbus.spider.spider.entity.dto;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Series;

import lombok.Data;

@Data
public class MovieSeriesDTO {
    private Movie movie;
    private Series series;
}
