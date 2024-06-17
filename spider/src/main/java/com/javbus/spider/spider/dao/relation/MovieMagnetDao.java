package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieMagnetRelation;

@Mapper
public interface MovieMagnetDao {

    void addMovieMagnetRelation(MovieMagnetRelation relation);

    void addMovieMagnetRelations(List<MovieMagnetRelation> relations);

    void updateMovieMagnetRelation(MovieMagnetRelation relation);

    void updateMovieMagnetRelations(List<MovieMagnetRelation> relation);

    List<MovieMagnetRelation> queryRelationsByMovieId(Integer movieId);

    List<MovieMagnetRelation> queryRelationsByMagnetId(Integer magnetId);
}
