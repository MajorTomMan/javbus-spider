package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarStudioRelation;

@Mapper
public interface StarStudioDao {
    void addStarStudioRelation(StarStudioRelation relation);

    void deleteStarStudioRelation(int starId, int studioId);
}
