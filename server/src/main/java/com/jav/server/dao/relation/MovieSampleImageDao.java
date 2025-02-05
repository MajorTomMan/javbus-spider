package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieSampleImageRelation;

@Mapper
public interface MovieSampleImageDao {
    void addMovieSampleImageRelation(MovieSampleImageRelation relation);

    void deleteMovieSampleImageRelation(Integer movieId, Integer sampleImageId);

    void addMovieSampleImageRelations(List<MovieSampleImageRelation> relations);

    List<MovieSampleImageRelation> queryMovieSampleImageRelations(Integer movieId,List<Integer> sampleImageIds);

    List<MovieSampleImageRelation> queryMovieSampleImageRelationsByMovieId(Integer movieId);

    void updateMovieSampleImageRelations(List<MovieSampleImageRelation> relations);
}
