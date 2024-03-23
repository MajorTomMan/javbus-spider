package com.javbus.spider.spider.service.relation.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.LabelDao;
import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.relation.MovieLabelDao;
import com.javbus.spider.spider.entity.base.Label;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.relation.MovieLabelRelation;
import com.javbus.spider.spider.entity.vo.MovieLabelVO;
import com.javbus.spider.spider.entity.dto.MovieLabelDTO;
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
    public void saveRelation(MovieLabelDTO dto) {
        // TODO Auto-generated method stub
        Movie movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        if (movie == null) {
            movieDao.saveMovie(dto.getMovie());
            movie = movieDao.queryMovieByLink(dto.getMovie().getLink());
        } else {
            dto.getMovie().setId(movie.getId());
            movieDao.updateMovie(dto.getMovie());
        }
        Label label = labelDao.queryLabelByName(dto.getLabel().getName());
        if (label == null) {
            labelDao.save(dto.getLabel());
            label = labelDao.queryLabelByName(dto.getLabel().getName());
        } else {
            dto.getLabel().setId(label.getId());
            labelDao.update(dto.getLabel());
        }
        MovieLabelRelation movieLabelRelation = movieLabelDao.queryMovieLabelRelation(movie.getId(), label.getId());
        if (movieLabelRelation == null) {
            MovieLabelRelation relation = new MovieLabelRelation();
            relation.setLabelId(label.getId());
            relation.setMovieId(movie.getId());
            movieLabelDao.addMovieLabelRelation(relation);
        }

    }

    @Override
    public MovieLabelVO queryRelations(Integer movieId) {
        // TODO Auto-generated method stub
        MovieLabelRelation relation = movieLabelDao.queryMovieLabelRelationByMovieId(movieId);
        if (relation == null) {
            return null;
        }
        MovieLabelVO vo = new MovieLabelVO();
        Movie movie = movieDao.queryMovieById(movieId);
        vo.setMovie(movie);
        Label label = labelDao.queryLabelById(relation.getLabelId());
        vo.setLabel(label);
        return vo;
    }

}
