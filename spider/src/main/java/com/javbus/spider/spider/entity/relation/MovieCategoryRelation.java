package com.javbus.spider.spider.entity.relation;

import java.util.List;

import lombok.Data;

@Data
public class MovieCategoryRelation {
    private Integer id;
    private Integer movieId;
    private Integer categoryId;
}
