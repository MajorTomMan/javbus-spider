package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.ActressCategoryRelation;


@Mapper
public interface ActressCategoryDao {
    void addActressCategoryRelation(ActressCategoryRelation relation);
    void addActressCategoryRelations(List<ActressCategoryRelation> relations);
    void deleteActressCategoryRelation(Integer actressId, Integer categoryId);
    List<ActressCategoryRelation> queryActressCategoryRelations(List<Integer> actressIds,List<Integer> categoryIds);
    List<ActressCategoryRelation> queryActressCategoryRelationsByActressId(Integer actressId);

    void updateActressCategoryRelations(List<ActressCategoryRelation> relations);
}
