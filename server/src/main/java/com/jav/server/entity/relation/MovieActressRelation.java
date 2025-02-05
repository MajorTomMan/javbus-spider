package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class MovieActressRelation {
    private Integer id;
    private Integer movieId;
    private Integer actressId;
}
