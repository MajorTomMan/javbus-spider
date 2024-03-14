package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieDirectorRelation;

@Mapper
public interface MovieDirectorDao {
    void addMovieDirectorRelation(MovieDirectorRelation relation);

    void deleteMovieDirectorRelation(Integer movidId, Integer directorId);

    MovieDirectorRelation queryMovieDirectorRelation(Integer movieId, Integer directorId);
}
