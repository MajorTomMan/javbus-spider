package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Series;

public interface SeriesService {

    void saveSeries(Series series);

    Series querySeriesById(Integer id);

    Series querySeriesByName(String name);

}
