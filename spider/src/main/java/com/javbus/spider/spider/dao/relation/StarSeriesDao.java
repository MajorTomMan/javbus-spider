package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarSeriesRelation;

@Mapper
public interface StarSeriesDao {
    void addStarSeriesRelation(StarSeriesRelation relation);

    void deleteStarSeriesRelation(int starId, int seriesId);
}
