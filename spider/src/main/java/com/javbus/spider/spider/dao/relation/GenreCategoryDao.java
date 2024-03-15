package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.GenreCategoryRelation;
/**
 * GenreCategoryDao
 */
@Mapper
public interface GenreCategoryDao {
    void addGenreCategoryRelation(GenreCategoryRelation relation);

    void addGenreCategoryRelations(List<GenreCategoryRelation> relations);

    void deleteGenreCategoryRelation(Integer genreId, Integer categoryId);
    List<GenreCategoryRelation> queryGenreCategoryRelations(Integer genreId,List<Integer> categoryIds);
    List<GenreCategoryRelation> queryGenreCategoryRelationsByGenreId(Integer genreId);
}