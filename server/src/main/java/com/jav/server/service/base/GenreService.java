package com.jav.server.service.base;

import com.jav.server.entity.base.Genre;

public interface GenreService {

    void saveGenre(Genre genre);

    Genre queryGenreById(Integer id);

    Genre queryGenreByName(String name);
    
}
