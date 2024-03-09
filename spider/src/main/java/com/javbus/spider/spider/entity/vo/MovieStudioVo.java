package com.javbus.spider.spider.entity.vo;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;


@Data
public class MovieStudioVo {
    private Movie movie;
    private Studio studio;
}
