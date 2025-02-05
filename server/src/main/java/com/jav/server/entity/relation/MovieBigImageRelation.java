package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class MovieBigImageRelation {
    private Integer id;
    private Integer movieId;
    private Integer bigImageId;
}
