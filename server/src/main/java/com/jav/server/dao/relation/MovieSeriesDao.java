package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieSeriesRelation;

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