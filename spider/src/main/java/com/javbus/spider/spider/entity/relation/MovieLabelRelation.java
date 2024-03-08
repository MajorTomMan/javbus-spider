package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class MovieLabelRelation {
    private Integer id;
    private Integer movieId;
    private Integer labelId;
}
