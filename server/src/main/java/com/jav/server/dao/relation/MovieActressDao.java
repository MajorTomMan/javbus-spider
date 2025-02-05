package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieActressRelation;

@Mapper
public interface MovieActressDao {
    void addMovieActressRelation(MovieActressRelation relation);
    void addMovieActressRelations(List<MovieActressRelation> relations);
    void deleteMovieActressRelation(Integer movieId, Integer actressId);
    MovieActressRelation queryMovieActressRelation(Integer movieId, Integer actressId);
    List<MovieActressRelation> queryMovieActressRelations(Integer movieId, List<Integer> actressIds);
    List<MovieActressRelation> queryMovieActressRelationByMovieId(Integer movieId);

    void updateMovieActressRelations(List<MovieActressRelation> relations);
}
