package com.javbus.spider.spider.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.CategoryDao;
import com.javbus.spider.spider.dao.DirectorDao;
import com.javbus.spider.spider.dao.LabelDao;
import com.javbus.spider.spider.dao.MovieDao;
import com.javbus.spider.spider.dao.SeriesDao;
import com.javbus.spider.spider.dao.StarDao;
import com.javbus.spider.spider.dao.StudioDao;
import com.javbus.spider.spider.entity.Movie;
import com.javbus.spider.spider.service.MovieService;

@Service
public class MovieServiceImpl implements MovieService {
    @Autowired
    private StudioDao studioDao;
    @Autowired
    private StarDao starDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private LabelDao labelDao;
    @Autowired
    private CategoryDao categoryDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveMovie(Movie movie) {
        // TODO Auto-generated method stub
    }
}
