package com.jav.server.entity.relation;


import lombok.Data;

@Data
public class MovieSampleImageRelation {
    private Integer id;
    private Integer movieId;
    private Integer sampleImageId;
}
