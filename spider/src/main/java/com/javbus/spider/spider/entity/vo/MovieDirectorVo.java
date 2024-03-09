package com.javbus.spider.spider.entity.vo;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieDirectorVo {
    private Movie movie;
    private Director director;
}
