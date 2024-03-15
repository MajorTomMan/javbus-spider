package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Movie;

public interface MovieService {
    void saveMovie(Movie movie);

    Movie queryMovieById(Integer id);

    Movie queryMovieByCode(String code);
}
