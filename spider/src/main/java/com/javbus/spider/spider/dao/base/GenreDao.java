package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Genre;

@Mapper
public interface GenreDao {
    void saveGenre(Genre genre);

    void saveGenres(List<Genre> genres);

    Genre queryGenreById(Integer id);

    void updateGenre(Genre genre);

    void deleteGenre(Integer id);

    Integer queryGenreIdByName(String name);

    Genre queryGenreByName(String name);
}
