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
        Movie movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        if (movie == null) {
            movieDao.saveMovie(vo.getMovie());
            movie = movieDao.queryMovieByCode(vo.getMovie().getCode());
        }
        List<Star> stars = vo.getStars();
        List<String> names = stars.stream().map((star) -> {
            return star.getName();
        }).collect(Collectors.toList());
        List<Integer> starIds = starDao.queryStarIdsByNames(names);
        if (starIds == null || starIds.isEmpty()) {
            starDao.saveStars(stars);
            starIds = starDao.queryStarIdsByNames(names);
        }
        final Movie final_movie = movie;
        List<MovieStarRelation> movieStarRelations = movieStarDao.queryMovieStarRelations(movie.getId(), starIds);
        if(movieStarRelations==null||movieStarRelations.isEmpty()){
            List<MovieStarRelation> relations = starIds.stream().map((id) -> {
                MovieStarRelation relation = new MovieStarRelation();
                relation.setMovieId(final_movie.getId());
                relation.setStarId(id);
                return relation;
            }).collect(Collectors.toList());
            movieStarDao.addMovieStarRelations(relations);
        }
    }

}
