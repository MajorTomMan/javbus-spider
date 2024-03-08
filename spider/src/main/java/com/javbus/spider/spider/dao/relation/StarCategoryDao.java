package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.StarCategoryRelation;


@Mapper
public interface StarCategoryDao {
    void addStarCategoryRelation(StarCategoryRelation relation);

    void deleteStarCategoryRelation(int starId, int categoryId);

    void addStarCategoryRelations(List<StarCategoryRelation> relations);
}
