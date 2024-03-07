package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Director;

@Mapper
public interface DirectorDao {
    void save(Director director);
    int queryDirectorById(Integer id);
    int update(Director director);
    int delete(Integer id);
}
