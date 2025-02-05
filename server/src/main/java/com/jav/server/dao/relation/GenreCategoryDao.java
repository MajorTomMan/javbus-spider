package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.GenreCategoryRelation;
/**
 * GenreCategoryDao
 */
@Mapper
public interface GenreCategoryDao {
    void addGenreCategoryCensoredRelation(GenreCategoryRelation relation);

    void addGenreCategoryCensoredRelations(List<GenreCategoryRelation> relations);
    void addGenreCategoryUncensoredRelation(GenreCategoryRelation relation);

    void addGenreCategoryUncensoredRelations(List<GenreCategoryRelation> relations);


    void deleteGenreCategoryCensoredRelation(Integer genreId, Integer categoryId);
    void deleteGenreCategoryUncensoredRelation(Integer genreId, Integer categoryId);
    List<GenreCategoryRelation> queryGenreCategoryUncensoredRelations(Integer genreId,List<Integer> categoryIds);
    List<GenreCategoryRelation> queryGenreCategoryUncensoredRelationsByGenreId(Integer genreId);
    List<GenreCategoryRelation> queryGenreCategoryCensoredRelations(Integer genreId,List<Integer> categoryIds);
    List<GenreCategoryRelation> queryGenreCategoryCensoredRelationsByGenreId(Integer genreId);
    void updateGenreCategoryCensoredRelations(List<GenreCategoryRelation> relations);

    void updateGenreCategoryUncensoredRelations(List<GenreCategoryRelation> relations);
}