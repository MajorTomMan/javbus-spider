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
import com.javbus.spider.spider.dao.relation.MovieCategoryDao;
import com.javbus.spider.spider.dao.relation.MovieDirectorDao;
import com.javbus.spider.spider.dao.relation.MovieStarDao;
import com.javbus.spider.spider.dao.relation.StarDirectorDao;
import com.javbus.spider.spider.dao.relation.StarSeriesDao;
import com.javbus.spider.spider.dao.relation.StarStudioDao;
import com.javbus.spider.spider.entity.request.MovieRequest;
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
    @Autowired
    private MovieCategoryDao movieCategoryDao;
    @Autowired
    private MovieStarDao movieStarDao;
    @Autowired
    private MovieDirectorDao movieDirectorDao;
    @Autowired
    private StarDirectorDao starDirectorDao;
    @Autowired
    private StarStudioDao starStudioDao;
    @Autowired
    private StarSeriesDao starSeriesDao;
    @Override
    public void saveMovie(MovieRequest movie) {
        // TODO Auto-generated method stub
        movieDao.save(movie);
    }
}
