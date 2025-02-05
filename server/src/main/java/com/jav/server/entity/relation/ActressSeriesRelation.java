package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class ActressSeriesRelation {
    private Integer id;
    private Integer actressId;
    private Integer seriesId;
}
