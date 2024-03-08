package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class MovieStudioRelation {
    private Integer id;
    private Integer movieId;
    private Integer studioId;
}
