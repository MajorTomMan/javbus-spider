package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.LabelDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieLabelDao;
import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieLabelRelation;
import com.javbus.spider.spider.entity.vo.MovieLabelVo;
import com.javbus.spider.spider.service.relation.MovieLabelRelationService;

@Service
public class MovieLabelRelationServiceImpl implements MovieLabelRelationService {
    @Autowired
    private MovieLabelDao movieLabelDao;
    @Autowired
    private LabelDao labelDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveRelation(MovieLabelVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if(movie==null){
            movieDao.saveMovie(vo.getMovie());
            movie=movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        Label label=labelDao.queryLabelByName(vo.getLabel().getName());
        if(label==null){
            labelDao.save(vo.getLabel());
            label=labelDao.queryLabelByName(vo.getLabel().getName());
        }
        MovieLabelRelation movieDirectorRelation = movieLabelDao.queryMovieDirectorRelation(movie.getId(),label.getId());
        if(movieDirectorRelation==null){
            MovieLabelRelation relation=new MovieLabelRelation();
            relation.setLabelId(label.getId());
            relation.setMovieId(movie.getId());
            movieLabelDao.addMovieLabelRelation(relation);
        }

    }
    
}
