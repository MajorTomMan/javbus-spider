package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieDirectorDao;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieDirectorRelation;
import com.javbus.spider.spider.entity.vo.MovieDirectorVo;
import com.javbus.spider.spider.service.relation.MovieDirectorRelationService;


@Service
public class MovieDirectorRelationServiceImpl implements MovieDirectorRelationService {
    @Autowired
    private MovieDirectorDao movieDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private MovieDao movieDao;
    @Override
    public void saveRelaton(MovieDirectorVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());;
        if(movie==null){
            movieDao.saveMovie(vo.getMovie());
            movie=movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        Director director = directorDao.queryDirectorByName(vo.getDirector().getName());
        if(director==null){
            directorDao.save(vo.getDirector());
            director=directorDao.queryDirectorByName(vo.getDirector().getName());
        }
        MovieDirectorRelation relation=new MovieDirectorRelation();
        relation.setMovieId(movie.getId());
        relation.setDirectorId(director.getId());
        movieDirectorDao.addMovieDirectorRelation(relation);
    }
}
