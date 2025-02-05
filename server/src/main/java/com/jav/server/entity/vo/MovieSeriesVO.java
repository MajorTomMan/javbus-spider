package com.jav.server.entity.vo;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Series;

import lombok.Data;

@Data
public class MovieSeriesVO {
    Movie movie;
    Series series;
}
