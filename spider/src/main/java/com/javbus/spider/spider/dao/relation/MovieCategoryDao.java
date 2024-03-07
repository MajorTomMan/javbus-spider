package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieCategoryRelation;

@Mapper
public interface MovieCategoryDao {
    void addMovieCategoryRelation(MovieCategoryRelation relation);

    void deleteMovieCategoryRelation(int movieId, int categoryId);
}