package com.jav.server.service.base;

import com.jav.server.entity.base.Series;

public interface SeriesService {

    void saveSeries(Series series);

    Series querySeriesById(Integer id);

    Series querySeriesByName(String name);

}
