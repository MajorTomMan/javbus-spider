package com.javbus.spider.spider.dao.base;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.javbus.spider.spider.entity.base.Category;

@Mapper
public interface CategoryDao {
    Category queryCategoryById(Integer id);
    Category queryCategoryByName(String name);
    List<Category> queryCategoriesByNames(List<String> names);
    List<Integer> queryCategoryIdsByNames(List<String> names);
    List<Category> queryCategoriesByIds(List<Integer> categoryIds);
    void saveCategory(Category category);
    void saveCategories(List<Category> categories);
    void delete(Integer id);
    void update(Category category);
    void updateCategories(List<Category> categories);
}
