package com.javbus.spider.spider.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Series;

@Mapper
public interface SeriesDao {
    Series querySeriesById(Integer id);
    Series querySeriesByName(String name);
    void save(Series series);

    void delete(Integer id);

    void update(Series series);
}
