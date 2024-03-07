package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarDirectorRelation;

@Mapper
public interface StarDirectorDao {
    void addStarDirectorRelation(StarDirectorRelation relation);

    void deleteStarDirectorRelation(int starId, int directorId);
}
