package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Series;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class ActressSeriesDTO {
    private List<Actress> actress;
    private Series series;
}
