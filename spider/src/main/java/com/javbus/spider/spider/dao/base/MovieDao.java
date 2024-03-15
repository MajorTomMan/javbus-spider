package com.javbus.spider.spider.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Movie;

@Mapper
public interface MovieDao {
    void saveMovie(Movie movie);
    
    Movie queryMovieByTitle(String title);

    Movie queryMovieById(Integer id);
    
    Movie queryMovieByCode(String code);
    void updateMovie(Movie movie);
    void updateMovieByCode(Movie movie);
    void deleteMovie(Integer id);

}
