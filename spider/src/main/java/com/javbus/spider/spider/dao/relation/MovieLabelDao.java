package com.javbus.spider.spider.dao.relation;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieLabelRelation;

@Mapper
public interface MovieLabelDao {
    void addMovieLabelRelation(MovieLabelRelation relation);

    void deleteMovieLabelRelation(int movieId, int labelId);
}
