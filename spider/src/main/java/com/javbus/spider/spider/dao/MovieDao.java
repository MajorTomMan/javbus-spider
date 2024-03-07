package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Movie;

@Mapper
public interface MovieDao {
    void saveMovie(Movie movie);
}
