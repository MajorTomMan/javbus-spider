package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieSeriesRelation;

/**
 * MovieSeriesDao
 */
@Mapper
public interface MovieSeriesDao {
    void addMovieSeriesRelation(MovieSeriesRelation relation);

    void deleteMovieSeriesRelation(Integer movieId, Integer seriesId);
    MovieSeriesRelation queryMovieSeriesRelation(Integer movieId, Integer seriesId);
}