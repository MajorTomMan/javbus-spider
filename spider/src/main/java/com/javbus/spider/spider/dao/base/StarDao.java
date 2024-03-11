package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Star;

@Mapper
public interface StarDao {
    void saveStar(Star star);

    Integer queryStarIdByName(Integer id);

    Star queryStarById(Integer id);

    Star queryStarByName(String name);

    List<Integer> queryStarIdsByNames(List<String> names);

    void update(Star star);

    void delete(Integer id);

    void saveStars(List<Star> stars);
}
