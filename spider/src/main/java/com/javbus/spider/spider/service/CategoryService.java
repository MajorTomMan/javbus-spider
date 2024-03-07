package com.javbus.spider.spider.service;

import java.util.List;

import com.javbus.spider.spider.entity.Category;

public interface CategoryService {

    void saveCategory(Category category);

    void saveCategories(List<Category> categories);
    
}
