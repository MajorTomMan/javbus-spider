package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class MovieActressDTO {
    private Movie movie;
    private List<Actress> actress;
}
