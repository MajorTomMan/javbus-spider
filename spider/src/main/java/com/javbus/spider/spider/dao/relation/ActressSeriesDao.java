package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.ActressSeriesRelation;

@Mapper
public interface ActressSeriesDao {
    void addActressSeriesRelation(ActressSeriesRelation relation);

    void addActressSeriesRelations(List<ActressSeriesRelation> relations);

    void deleteActressSeriesRelation(Integer movieId, Integer seriesId);

    ActressSeriesRelation queryActressSeriesRelation(Integer movieId, Integer seriesId);

    List<ActressSeriesRelation> queryActressSeriesRelations(List<Integer> actressIds, Integer seriesId);

    List<ActressSeriesRelation> queryActressSeriesRelationsByActressId(Integer actressId);

    void updateActressSeriesRelation(List<ActressSeriesRelation> relations);
}
