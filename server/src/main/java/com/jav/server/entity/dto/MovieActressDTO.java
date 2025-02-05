package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class MovieActressDTO {
    private Movie movie;
    private List<Actress> actress;
}
