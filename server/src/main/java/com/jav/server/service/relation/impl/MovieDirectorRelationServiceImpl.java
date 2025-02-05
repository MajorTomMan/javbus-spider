package com.jav.server.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.DirectorDao;
import com.jav.server.dao.base.MovieDao;
import com.jav.server.dao.relation.MovieDirectorDao;
import com.jav.server.entity.base.Director;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.relation.MovieDirectorRelation;
import com.jav.server.entity.vo.MovieDirectorVO;
import com.jav.server.entity.dto.MovieDirectorDTO;
import com.jav.server.service.relation.MovieDirectorRelationService;

@Service
public class MovieDirectorRelationServiceImpl implements MovieDirectorRelationService {
    @Autowired
    private MovieDirectorDao movieDirectorDao;
    @Autowired
    private DirectorDao directorDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    @Transactional
    public void saveRelaton(MovieDirectorDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        Director director = directorDao.queryDirectorByName(dto.getDirector().getName());
        if (director == null) {
            directorDao.save(dto.getDirector());
            director = directorDao.queryDirectorByName(dto.getDirector().getName());
        } else {
            dto.getDirector().setId(director.getId());
            directorDao.update(dto.getDirector());
        }
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
