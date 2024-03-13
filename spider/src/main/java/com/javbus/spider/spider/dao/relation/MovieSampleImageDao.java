package com.javbus.spider.spider.dao.relation;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.relation.MovieSampleImageRelation;

@Mapper
public interface MovieSampleImageDao {
    void addMovieSampleImageRelation(MovieSampleImageRelation relation);

    void deleteMovieSampleImageRelation(int movieId, int sampleImageId);

    void addMovieSampleImageRelations(List<MovieSampleImageRelation> relations);

    List<MovieSampleImageRelation> queryMovieSampleImageRelatios(Integer movieId,List<Integer> categoryIds);
}
