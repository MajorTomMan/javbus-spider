package com.jav.server.dao.base;

import org.apache.ibatis.annotations.Mapper;

import com.jav.server.entity.base.Label;


@Mapper
public interface LabelDao {
    void save(Label label);

    Label queryLabelById(Integer id);

    void update(Label label);

    void delete(Integer id);

    Label queryLabelByName(String name);
}
