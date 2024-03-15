package com.javbus.spider.spider.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.service.base.MovieService;

@Service
public class MovieServiceImpl implements MovieService {
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveMovie(Movie movie) {
        // TODO Auto-generated method stub
        movieDao.saveMovie(movie);
    }
    @Override
    public Movie queryMovieById(Integer id) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieById(id);
    }
    @Override
    public Movie queryMovieByCode(String code) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieByCode(code);
    }
}
