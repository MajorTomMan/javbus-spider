package com.javbus.spider.spider.entity.dto;

import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieLabelDTO {
    private Movie movie;
    private Label label;
}
