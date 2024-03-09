package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class StarSeriesVo {
    private List<Star> stars;
    private Series series;
}
