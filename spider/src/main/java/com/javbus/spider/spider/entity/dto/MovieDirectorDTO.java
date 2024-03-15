package com.javbus.spider.spider.entity.dto;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieDirectorDTO {
    private Movie movie;
    private Director director;
}
