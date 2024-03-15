package com.javbus.spider.spider.entity.dto;

import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieBigImageDTO {
    private Movie movie;
    private BigImage bigImage;
}
