package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressSeriesDTO {
    private List<Actress> actress;
    private Series series;
}
