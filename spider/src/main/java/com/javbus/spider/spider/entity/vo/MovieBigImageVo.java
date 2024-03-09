package com.javbus.spider.spider.entity.vo;

import com.javbus.spider.spider.entity.base.BigImage;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieBigImageVo {
    private Movie movie;
    private BigImage bigImage;
}
