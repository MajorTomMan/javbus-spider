package com.javbus.spider.spider.dao.relation;

import java.util.List;

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

    MovieSeriesRelation queryMovieSeriesRelationByMovieId(Integer movieId);

    void updateMovieSeriesRelations(List<MovieSeriesRelation> relations);
}