package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieCategoryRelation;

@Mapper
public interface MovieCategoryDao {
    void addMovieCategoryRelation(MovieCategoryRelation relation);

    void addMovieCategoryRelations(List<MovieCategoryRelation> relations);

    void deleteMovieCategoryRelation(Integer movieId, Integer categoryId);
    List<MovieCategoryRelation> queryMovieCategoryRelations(Integer movieId,List<Integer> categoryIds);
}