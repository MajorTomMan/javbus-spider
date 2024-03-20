package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class MovieActressVO {
    Movie movie;
    List<Actress> actresses;
}
