package com.jav.server.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.base.Movie;

@Mapper
public interface MovieDao {
    void saveMovie(Movie movie);
    
    Movie queryMovieByTitle(String title);

    Movie queryMovieById(Integer id);
    
    Movie queryMovieByCode(String code);
    void updateMovie(Movie movie);
    void updateMovieByCode(Movie movie);
    void deleteMovie(Integer id);

    List<String> queryMovieCodes(Boolean isCensored, Integer pageSize, Integer offset);

    Movie queryMovieByLink(String link);

}
