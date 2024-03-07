package com.javbus.spider.spider.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Star;

@Mapper
public interface StarDao {
    void save(Star star);
    void queryStarById(Integer id);
    void queryStarByName(Integer id);
    void update(Star star);
    void delete(Integer id);
    void saveStars(List<Star> stars);
}
