package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Label;


@Mapper
public interface LabelDao {
    void save(Label label);

    int queryDirectorById(Integer id);

    int update(Label label);

    int delete(Integer id);
}
