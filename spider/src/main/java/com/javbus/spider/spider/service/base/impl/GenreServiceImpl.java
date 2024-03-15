package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.GenreDao;
import com.javbus.spider.spider.entity.base.Genre;
import com.javbus.spider.spider.service.base.GenreService;

@Service
public class GenreServiceImpl implements GenreService {
    @Autowired
    private GenreDao genreDao;
    @Override
    public void saveGenre(Genre genre) {
        // TODO Auto-generated method stub
        genreDao.saveGenre(genre);
    }
    @Override
    public Genre queryGenreById(Integer id) {
        // TODO Auto-generated method stub
        return genreDao.queryGenreById(id);
    }
    @Override
    public Genre queryGenreByName(String name) {
        // TODO Auto-generated method stub
        return genreDao.queryGenreByName(name);
    }

}
