package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieDirectorRelation;

@Mapper
public interface MovieDirectorDao {
    void addMovieDirectorRelation(MovieDirectorRelation relation);

    void deleteMovieDirectorRelation(Integer movidId, Integer directorId);

    MovieDirectorRelation queryMovieDirectorRelation(Integer movieId, Integer directorId);

    MovieDirectorRelation queryMovieDirectorRelationByMovieId(Integer movieId);

    void updateMovieDirectorRelations(List<MovieDirectorRelation> relations);
}
