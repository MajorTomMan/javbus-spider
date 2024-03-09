package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieSeriesRelation;

/**
 * MovieSeriesDao
 */
@Mapper
public interface MovieSeriesDao {
    void addMovieSeriesRelation(MovieSeriesRelation relation);

    void deleteMovieSeriesRelation(int movieId, int seriesId);
}