package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieBigImageRelation;


@Mapper
public interface MovieBigImageDao {
    void addMovieBigImageRelation(MovieBigImageRelation relation);

    void deleteMovieBigImageRelation(Integer movieId, Integer bigImageId);
    MovieBigImageRelation queryMovieBigImageRelation(Integer movieId, Integer bigImageId);
    MovieBigImageRelation queryMovieBigImageRelationByMovieId(Integer movieId);

    void updateMovieBigImageRelations(List<MovieBigImageRelation> relations);
}
