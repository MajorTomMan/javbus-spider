package com.jav.server.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.relation.MovieStudioRelation;

@Mapper
public interface MovieStudioDao {
    void addMovieStudioRelation(MovieStudioRelation relation);

    void deleteMovieStudioRelation(Integer movieId, Integer studioId);
    MovieStudioRelation queryMovieStudioRelation(Integer movieId, Integer studioId);

    MovieStudioRelation queryMovieStudioRelationByMovieId(Integer movieId);

    void updateMovieStudioRelations(List<MovieStudioRelation> relations);
}
