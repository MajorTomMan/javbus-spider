package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieStudioRelation;

@Mapper
public interface MovieStudioDao {
    void addMovieStudioRelation(MovieStudioRelation relation);

    void deleteMovieStudioRelation(Integer movieId, Integer studioId);
    MovieStudioRelation queryMovieStudioRelation(Integer movieId, Integer studioId);
}
