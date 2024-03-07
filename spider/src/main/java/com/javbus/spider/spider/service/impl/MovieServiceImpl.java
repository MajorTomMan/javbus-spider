package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.MovieDao;
import com.javbus.spider.spider.entity.Movie;
import com.javbus.spider.spider.service.MovieService;

@Service
public class MovieServiceImpl implements MovieService {
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveMovie(Movie movie) {
        // TODO Auto-generated method stub
        movieDao.saveMovie(movie);
    }
}
