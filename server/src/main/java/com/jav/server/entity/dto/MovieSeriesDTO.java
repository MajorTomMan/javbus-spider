package com.jav.server.entity.dto;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Series;

import lombok.Data;

@Data
public class MovieSeriesDTO {
    private Movie movie;
    private Series series;
}
