package com.jav.server.entity.relation;


import lombok.Data;

@Data
public class MovieCategoryRelation {
    private Integer id;
    private Integer movieId;
    private Integer categoryId;
}
