package com.javbus.spider.spider.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.Category;

@Mapper
public interface CategoryDao {
    Category queryCategoryById(Integer id);
    Category queryCategoryByName(String name);
    void saveCategory(Category category);
    void saveCategories(List<Category> categories);
    void delete(Integer id);

    void update(Category category);
}
