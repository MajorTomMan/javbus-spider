package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Director;

@Mapper
public interface DirectorDao {
    void save(Director director);
    Director queryDirectorById(Integer id);
    Director queryDirectorByName(String name);
    void update(Director director);
    void delete(Integer id);
}
