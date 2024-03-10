package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class StarCensorRelation {
    private Integer id;
    private Integer starId;
    private Boolean isCensored;
}