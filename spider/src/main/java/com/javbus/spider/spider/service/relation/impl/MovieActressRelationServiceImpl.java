package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.ActressDao;
import com.javbus.spider.spider.dao.relation.MovieActressDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Actress;
import com.javbus.spider.spider.entity.relation.MovieActressRelation;
import com.javbus.spider.spider.entity.vo.MovieActressVo;
import com.javbus.spider.spider.service.relation.MovieActressRelationService;

@Service
public class MovieActressRelationServiceImpl implements MovieActressRelationService {
    @Autowired
    private MovieActressDao movieActressDao;
    @Autowired
    private ActressDao ActressDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveRelation(MovieActressVo vo) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(vo.getMovie());
            movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        List<Actress> actresses = vo.getActress();
        List<String> names = actresses.stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> ActressIds = ActressDao.queryActressIdsByNames(names);
        if (ActressIds == null || ActressIds.isEmpty()) {
            ActressDao.saveActresses(actresses);
            ActressIds = ActressDao.queryActressIdsByNames(names);
        }
        List<MovieActressRelation> movieActressRelations = movieActressDao.queryMovieActressRelations(movie.getId(),
                ActressIds);
        if (movieActressRelations == null || movieActressRelations.isEmpty()) {
            final Movie final_movie = movie;
            List<MovieActressRelation> relations = ActressIds.stream().map((id) -> {
                MovieActressRelation relation = new MovieActressRelation();
                relation.setMovieId(final_movie.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            movieActressDao.addMovieActressRelations(relations);
        }
    }

}
