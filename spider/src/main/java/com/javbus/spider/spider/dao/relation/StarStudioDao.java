package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarStudioRelation;

@Mapper
public interface StarStudioDao {
    void addStarStudioRelation(StarStudioRelation relation);

    void deleteStarStudioRelation(int starId, int studioId);

    void addStarStudioRelations(List<StarStudioRelation> relations);
    StarStudioRelation queryStarStudioRelation(int starId, int studioId);
    List<StarStudioRelation> queryStarStudioRelations(List<Integer> starIds, Integer studioIds);
}
