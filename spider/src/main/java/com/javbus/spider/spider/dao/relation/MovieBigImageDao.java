package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieBigImageRelation;


@Mapper
public interface MovieBigImageDao {
    void addMovieBigImageRelation(MovieBigImageRelation relation);

    void deleteMovieBigImageRelation(int movieId, int bigImageId);
    MovieBigImageRelation queryMovieBigImageRelation(int movieId, int bigImageId);
}
