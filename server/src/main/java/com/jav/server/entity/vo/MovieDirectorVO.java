package com.jav.server.entity.vo;

import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieDirectorVO {
    Movie movie;
    Director director;
}
