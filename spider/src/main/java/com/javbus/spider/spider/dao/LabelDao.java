package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Label;


@Mapper
public interface LabelDao {
    void save(Label label);

    Label queryDirectorById(Integer id);

    void update(Label label);

    void delete(Integer id);
}
