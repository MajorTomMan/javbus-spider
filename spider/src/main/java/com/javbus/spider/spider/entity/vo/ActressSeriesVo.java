package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressSeriesVO {
    Actress actress;
    List<Series> series;
}
