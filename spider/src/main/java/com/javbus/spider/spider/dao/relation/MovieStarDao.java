package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieStarRelation;

@Mapper
public interface MovieStarDao {
    void addMovieStarRelation(MovieStarRelation relation);
    
    void deleteMovieStarRelation(int movieId, int starId);
}
