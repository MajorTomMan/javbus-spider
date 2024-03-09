package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieCategoryRelation;

@Mapper
public interface MovieCategoryDao {
    void addMovieCategoryRelation(MovieCategoryRelation relation);
    void addMovieCategoryRelations(List<MovieCategoryRelation> relation);

    void deleteMovieCategoryRelation(int movieId, int categoryId);
}