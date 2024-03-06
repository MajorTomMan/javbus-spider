package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Star;

@Mapper
public interface StarDao {
    void saveStar(Star star);
}
