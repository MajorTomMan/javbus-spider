package com.jav.server.entity.relation;

import lombok.Data;

@Data
public class MovieDirectorRelation {
    private Integer id;
    private Integer movieId;
    private Integer directorId;
}
