package com.javbus.spider.spider.service.relation.impl;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.base.MovieDao;
import com.javbus.spider.spider.dao.base.StarDao;
import com.javbus.spider.spider.dao.relation.MovieStarDao;
import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.Star;
import com.javbus.spider.spider.entity.relation.MovieStarRelation;
import com.javbus.spider.spider.entity.vo.MovieStarVo;
import com.javbus.spider.spider.service.relation.MovieStarRelationService;

@Service
public class MovieStarRelationServiceImpl implements MovieStarRelationService {
    @Autowired
    private MovieStarDao movieStarDao;
    @Autowired
    private StarDao starDao;
    @Autowired
    private MovieDao movieDao;

    @Override
    public void saveRelation(MovieStarVo vo) {
        // TODO Auto-generated method stub
        if (vo == null) {
            return;
        }
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            return;
        }
        List<Star> stars = vo.getStars();
        List<String> names = stars.stream().map((star) -> {
            return star.getName();
        }).collect(Collectors.toList());
        List<Integer> ids = starDao.queryStarIdsByNames(names);
        if (ids == null || ids.isEmpty()) {
            starDao.saveStars(stars);
            ids = starDao.queryStarIdsByNames(names);
        }
        List<MovieStarRelation> relations = ids.stream().map((id) -> {
            MovieStarRelation relation = new MovieStarRelation();
            relation.setMovieId(movie.getId());
            relation.setStarId(id);
            return relation;
        }).collect(Collectors.toList());
        movieStarDao.addMovieStarRelations(relations);
    }

}
