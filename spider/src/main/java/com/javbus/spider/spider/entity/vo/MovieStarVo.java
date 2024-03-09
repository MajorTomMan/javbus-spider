package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class MovieStarVo {
    private Movie movie;
    private List<Star> stars;
}
