package com.javbus.spider.spider.entity.relation;

import lombok.Data;

@Data
public class GenreCategoryRelation {
    private Integer id;
    private Integer genreId;
    private Integer categoryId;
    private Boolean isCensored;
}
