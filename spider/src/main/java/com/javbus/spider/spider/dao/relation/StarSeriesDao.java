package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarSeriesRelation;

@Mapper
public interface StarSeriesDao {
    void addStarSeriesRelation(StarSeriesRelation relation);
    void addStarSeriesRelations(List<StarSeriesRelation> relations);
    void deleteStarSeriesRelation(int movieId, int seriesId);
}
