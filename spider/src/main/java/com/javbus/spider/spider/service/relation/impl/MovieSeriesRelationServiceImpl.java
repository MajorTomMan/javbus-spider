package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SeriesDao;
import com.javbus.spider.spider.dao.relation.MovieSeriesDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Series;
import com.javbus.spider.spider.entity.relation.MovieSeriesRelation;
import com.javbus.spider.spider.entity.vo.MovieSeriesVo;
import com.javbus.spider.spider.service.relation.MovieSeriesRelationService;

@Service
public class MovieSeriesRelationServiceImpl implements MovieSeriesRelationService {
    @Autowired
    private MovieSeriesDao movieSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveRelaton(MovieSeriesVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if(movie==null){
            movieDao.saveMovie(vo.getMovie());
            movie=movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        Series series = seriesDao.querySeriesByName(vo.getSeries().getName());
        if(series==null){
            seriesDao.save(vo.getSeries());
            series = seriesDao.querySeriesByName(vo.getSeries().getName());
        }
        MovieSeriesRelation relation = new MovieSeriesRelation();
        relation.setMovieId(movie.getId());
        relation.setSeriesId(series.getId());
        movieSeriesDao.addMovieSeriesRelation(relation);
    }
    
}
