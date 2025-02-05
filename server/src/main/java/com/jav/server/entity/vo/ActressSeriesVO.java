package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Series;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class ActressSeriesVO {
    Actress actress;
    List<Series> series;
}
