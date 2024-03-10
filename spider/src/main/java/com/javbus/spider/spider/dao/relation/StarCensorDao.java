package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarCensorRelation;

@Mapper
public interface StarCensorDao {
    void addStarCensorRelation(StarCensorRelation relation);

    void deleteStarCensorRelation(int movieId, int sampleImageId);

    void addStarCensorRelations(List<StarCensorRelation> relations);
}
