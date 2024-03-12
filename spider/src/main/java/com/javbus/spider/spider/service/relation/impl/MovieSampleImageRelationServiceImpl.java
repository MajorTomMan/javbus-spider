package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.SampleImageDao;
import com.javbus.spider.spider.dao.relation.MovieSampleImageDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;
import com.javbus.spider.spider.entity.vo.MovieSampleImageVo;
import com.javbus.spider.spider.service.relation.MovieSampleImageRelationService;

@Service
public class MovieSampleImageRelationServiceImpl implements MovieSampleImageRelationService{
    @Autowired
    private MovieSampleImageDao movieSampleImageDao;
    @Autowired
    private SampleImageDao sampleImageDao;
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveRelation(MovieSampleImageVo vo) {
        // TODO Auto-generated method stub
        if(vo==null){
            return;
        }
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if(movie==null){
            movieDao.saveMovie(vo.getMovie());
            movie=movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        List<Integer> ids=sampleImageDao.querySampleImageIdsByLinks(vo.getSampleImages());
        if(ids==null||ids.isEmpty()){
            sampleImageDao.saveSampleImages(vo.getSampleImages());
            ids=sampleImageDao.querySampleImageIdsByLinks(vo.getSampleImages());
        }
        final Movie final_movie=movie;
        List<MovieSampleImageRelation> relations=ids.stream().map((id)->{
            MovieSampleImageRelation relation=new MovieSampleImageRelation();
            relation.setMovieId(final_movie.getId());
            relation.setSampleImageId(id);
            return relation;
        }).collect(Collectors.toList());
        movieSampleImageDao.addMovieSampleImageRelations(relations);
    }
    
}
