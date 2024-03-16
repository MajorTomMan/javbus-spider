package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.DirectorDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieDirectorDao;
import com.javbus.spider.spider.entity.base.Director;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieDirectorRelation;
import com.javbus.spider.spider.entity.vo.MovieDirectorVO;
import com.javbus.spider.spider.entity.dto.MovieDirectorDTO;
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
    public void saveRelaton(MovieDirectorDTO dto) {
        // TODO Auto-generated method stub
        movieDao.saveMovie(dto.getMovie());
        Movie movie = movieDao.queryMovieByCode(dto.getMovie().getCode());
        directorDao.save(dto.getDirector());
        Director director = directorDao.queryDirectorByName(dto.getDirector().getName());
        MovieDirectorRelation movieDirectorRelation = movieDirectorDao.queryMovieDirectorRelation(movie.getId(),
                director.getId());
        if (movieDirectorRelation == null) {
            MovieDirectorRelation relation = new MovieDirectorRelation();
            relation.setMovieId(movie.getId());
            relation.setDirectorId(director.getId());
            movieDirectorDao.addMovieDirectorRelation(relation);
        }
    }

    @Override
    public MovieDirectorVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        MovieDirectorRelation relation = movieDirectorDao.queryMovieDirectorRelationByMovieId(movieId);
        if (relation == null) {
            return null;
        }
        Movie movie = movieDao.queryMovieById(movieId);
        Director director = directorDao.queryDirectorById(relation.getDirectorId());
        MovieDirectorVO vo = new MovieDirectorVO();
        vo.setDirector(director);
        vo.setMovie(movie);
        return vo;
    }
}
