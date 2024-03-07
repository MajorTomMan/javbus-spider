package com.javbus.spider.spider.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.request.MovieRequest;

@Mapper
public interface MovieDao {
    void save(MovieRequest movie);
    
    MovieRequest queryMovieByTitle(String name);

    List<MovieRequest> queryMovieById(Integer id);

    void insert(MovieRequest movie);

    void update(MovieRequest movie);

    void delete(Integer id);
}
