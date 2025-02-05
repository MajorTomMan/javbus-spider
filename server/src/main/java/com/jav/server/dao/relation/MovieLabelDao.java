package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieLabelRelation;

@Mapper
public interface MovieLabelDao {
    void addMovieLabelRelation(MovieLabelRelation relation);

    void deleteMovieLabelRelation(Integer movieId, Integer labelId);
    MovieLabelRelation queryMovieLabelRelation(Integer movieId, Integer labelId);

    MovieLabelRelation queryMovieLabelRelationByMovieId(Integer movieId);

    void updateMovieLabelRelations(List<MovieLabelRelation> relations);
}
