package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarDirectorRelation;

@Mapper
public interface StarDirectorDao {
    void addStarDirectorRelation(StarDirectorRelation relation);
    void addStarDirectorRelations(List<StarDirectorRelation> relations);
    void deleteStarDirectorRelation(int starId, int directorId);
}
