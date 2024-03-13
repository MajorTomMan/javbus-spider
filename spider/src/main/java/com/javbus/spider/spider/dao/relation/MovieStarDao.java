package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieStarRelation;

@Mapper
public interface MovieStarDao {
    void addMovieStarRelation(MovieStarRelation relation);
    void addMovieStarRelations(List<MovieStarRelation> relations);
    void deleteMovieStarRelation(int movieId, int starId);
    MovieStarRelation queryMovieStarRelation(int movieId, int starId);
    List<MovieStarRelation> queryMovieStarRelations(int movieId, List<Integer> starIds);
}
