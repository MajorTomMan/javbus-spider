package com.javbus.spider.spider.entity.dto;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Studio;

import lombok.Data;


@Data
public class MovieStudioDTO {
    private Movie movie;
    private Studio studio;
}
