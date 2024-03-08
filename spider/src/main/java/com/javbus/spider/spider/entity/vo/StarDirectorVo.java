package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class StarDirectorVo {
    private List<Star> stars;
    private Director director;
}
