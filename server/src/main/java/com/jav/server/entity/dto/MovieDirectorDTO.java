package com.jav.server.entity.dto;

import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieDirectorDTO {
    private Movie movie;
    private Director director;
}
