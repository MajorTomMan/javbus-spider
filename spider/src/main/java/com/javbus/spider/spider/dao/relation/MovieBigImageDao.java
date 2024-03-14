package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieBigImageRelation;


@Mapper
public interface MovieBigImageDao {
    void addMovieBigImageRelation(MovieBigImageRelation relation);

    void deleteMovieBigImageRelation(Integer movieId, Integer bigImageId);
    MovieBigImageRelation queryMovieBigImageRelation(Integer movieId, Integer bigImageId);
}
