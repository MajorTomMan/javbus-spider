package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Series;

@Mapper
public interface SeriesDao {
    Series querySeriesById(Integer id);

    void save(Series series);

    void delete(Integer id);

    void update(Series series);
}
