package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieMagnetRelation;

@Mapper
public interface MovieMagnetDao {

    void saveRelation(MovieMagnetRelation relation);

    void saveRelations(List<MovieMagnetRelation> relations);

    void updateRelation(MovieMagnetRelation relation);

    void updateRelations(List<MovieMagnetRelation> relation);

    List<MovieMagnetRelation> queryRelationsByMovieId(Integer movieId);

    List<MovieMagnetRelation> queryRelationsByMagnetId(Integer magnetId);
}
