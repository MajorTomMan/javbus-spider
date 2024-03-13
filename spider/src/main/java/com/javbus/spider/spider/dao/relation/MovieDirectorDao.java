package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieDirectorRelation;

@Mapper
public interface MovieDirectorDao {
    void addMovieDirectorRelation(MovieDirectorRelation relation);

    void deleteMovieDirectorRelation(int starId, int directorId);

    MovieDirectorRelation queryMovieDirectorRelation(int starId, int directorId);
}
