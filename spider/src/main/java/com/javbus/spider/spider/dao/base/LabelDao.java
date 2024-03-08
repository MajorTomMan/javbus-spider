package com.javbus.spider.spider.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Label;


@Mapper
public interface LabelDao {
    void save(Label label);

    Label queryLabelById(Integer id);

    void update(Label label);

    void delete(Integer id);

    Label queryLabelByName(String name);
}
