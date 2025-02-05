package com.jav.server.service.relation.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.jav.server.dao.base.MovieDao;
import com.jav.server.dao.base.SeriesDao;
import com.jav.server.dao.relation.MovieSeriesDao;
import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Series;
import com.jav.server.entity.relation.MovieSeriesRelation;
import com.jav.server.entity.vo.MovieSeriesVO;
import com.jav.server.entity.dto.MovieSeriesDTO;
import com.jav.server.service.relation.MovieSeriesRelationService;

@Service
public class MovieSeriesRelationServiceImpl implements MovieSeriesRelationService {
    @Autowired
    private MovieSeriesDao movieSeriesDao;
    @Autowired
    private SeriesDao seriesDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    @Transactional
    public void saveRelaton(MovieSeriesDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        Series series = seriesDao.querySeriesByName(dto.getSeries().getName());
        if (series == null) {
            seriesDao.save(dto.getSeries());
            series = seriesDao.querySeriesByName(dto.getSeries().getName());
        } else {
            dto.getSeries().setId(series.getId());
            seriesDao.updateSeries(dto.getSeries());
        }
        MovieSeriesRelation movieSeriesRelation = movieSeriesDao.queryMovieSeriesRelation(movie.getId(),
                series.getId());
        if (movieSeriesRelation == null) {
            MovieSeriesRelation relation = new MovieSeriesRelation();
            relation.setMovieId(movie.getId());
            relation.setSeriesId(series.getId());
            movieSeriesDao.addMovieSeriesRelation(relation);
        }
    }

    @Override
    public MovieSeriesVO queryRelations(Integer movieId) {
        MovieSeriesVO vo = new MovieSeriesVO();
        Movie movie = movieDao.queryMovieById(movieId);
        vo.setMovie(movie);
        // TODO Auto-generated method stub
        MovieSeriesRelation relation = movieSeriesDao.queryMovieSeriesRelationByMovieId(movieId);
        if (relation == null) {
            vo.setSeries(null);
            return null;
        }
        Series series = seriesDao.querySeriesById(relation.getSeriesId());
        vo.setSeries(series);
        return vo;
    }

}
