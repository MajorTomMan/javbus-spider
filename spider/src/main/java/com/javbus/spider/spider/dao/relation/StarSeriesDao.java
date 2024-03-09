package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarSeriesRelation;

@Mapper
public interface StarSeriesDao {
    void addMovieSeriesRelation(StarSeriesRelation relation);
    void addMovieSeriesRelations(List<StarSeriesRelation> relations);
    void deleteMovieSeriesRelation(int movieId, int seriesId);
}
