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
    
}
