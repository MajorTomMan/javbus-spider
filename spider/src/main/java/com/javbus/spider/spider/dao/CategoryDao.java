package com.javbus.spider.spider.dao;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Category;

@Mapper
public interface CategoryDao {
    Category queryCategoryById(Integer id);

    void save(Category category);

    void delete(Integer id);

    void update(Category category);
}
