package com.javbus.spider.spider.service.base;

import com.javbus.spider.spider.entity.base.Genre;

public interface GenreService {

    void saveGenre(Genre genre);

    Genre queryGenreById(Integer id);

    Genre queryGenreByName(String name);
    
}
