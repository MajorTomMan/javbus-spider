package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class MovieActressVo {
    private Movie movie;
    private List<Actress> actress;
}
