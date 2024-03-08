package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class MovieStarVo {
    private String code;
    private List<Star> stars;
}
