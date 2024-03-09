package com.javbus.spider.spider.entity.vo;

import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;

@Data
public class MovieLabelVo {
    private Movie movie;
    private Label label;
}
