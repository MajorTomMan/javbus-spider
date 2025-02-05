package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class GenreCategoryRelation {
    private Integer id;
    private Integer genreId;
    private Integer categoryId;
    private Boolean isCensored;
}
