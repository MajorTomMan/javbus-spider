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
import com.javbus.spider.spider.entity.vo.MovieActressVO;
import com.javbus.spider.spider.entity.dto.MovieActressDTO;
import com.javbus.spider.spider.service.relation.MovieActressRelationService;

@Service
public class MovieActressRelationServiceImpl implements MovieActressRelationService {
    @Autowired
    private MovieActressDao movieActressDao;
    @Autowired
    private ActressDao actressDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveRelation(MovieActressDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        List<String> names = dto.getActress().stream().map((Actress) -> {
            return Actress.getName();
        }).collect(Collectors.toList());
        List<Integer> actressIds = actressDao.queryActressIdsByNames(names);
        if (actressIds.isEmpty() || actressIds.size() != dto.getActress().size()) {
            actressDao.saveActresses(dto.getActress());
            actressIds = actressDao.queryActressIdsByNames(names);
        } else {
            for (int i = 0; i < actressIds.size(); i++) {
                dto.getActress().get(i).setId(actressIds.get(i));
            }
            actressDao.updateActresses(dto.getActress());
        }
        List<MovieActressRelation> movieActressRelations = movieActressDao.queryMovieActressRelations(movie.getId(),
                actressIds);
        if (movieActressRelations == null || movieActressRelations.isEmpty()) {
            final Movie final_movie = movie;
            List<MovieActressRelation> relations = actressIds.stream().map((id) -> {
                MovieActressRelation relation = new MovieActressRelation();
                relation.setMovieId(final_movie.getId());
                relation.setActressId(id);
                return relation;
            }).collect(Collectors.toList());
            movieActressDao.addMovieActressRelations(relations);
        }
    }

    @Override
    public MovieActressVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        List<MovieActressRelation> relations = movieActressDao.queryMovieActressRelationByMovieId(movieId);
        if (relations == null || relations.isEmpty()) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(movieId);
        List<Integer> actressIds = relations.stream().map(relation -> {
            return relation.getActressId();
        }).collect(Collectors.toList());
        List<Actress> actresses = actressDao.queryActressesById(actressIds);
        MovieActressVO vo = new MovieActressVO();
        vo.setActresses(actresses);
        vo.setMovie(movie);
        return vo;
    }

}
