package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Genre;

@Mapper
public interface GenreDao {
    Genre queryGenreById(Integer id);

    void save(Genre genre);

    void delete(Integer id);

    void update(Genre genre);
}
