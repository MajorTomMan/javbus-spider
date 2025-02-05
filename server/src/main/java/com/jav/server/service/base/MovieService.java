package com.jav.server.service.base;

import com.jav.server.entity.base.Movie;

public interface MovieService {
    void saveMovie(Movie movie);

    Movie queryMovieById(Integer id);

    Movie queryMovieByCode(String code);
}
