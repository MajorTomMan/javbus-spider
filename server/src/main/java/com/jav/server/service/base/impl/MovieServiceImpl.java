package com.jav.server.service.base.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.MovieDao;
import com.jav.server.entity.base.Movie;
import com.jav.server.service.base.MovieService;

@Service
public class MovieServiceImpl implements MovieService {
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveMovie(Movie movie) {
        // TODO Auto-generated method stub
        Movie m = movieDao.queryMovieByLink(movie.getLink());
        if (m == null) {
            movieDao.saveMovie(movie);
        } else {
            movieDao.updateMovie(movie);
        }
    }

    @Override
    public Movie queryMovieById(Integer id) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieById(id);
    }

    @Override
    public Movie queryMovieByCode(String code) {
        // TODO Auto-generated method stub
        return movieDao.queryMovieByCode(code);
    }
}
