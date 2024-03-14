package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class ActressStudioRelation {
    private Integer id;
    private Integer actressId;
    private Integer studioId;
}