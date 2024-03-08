package com.javbus.spider.spider.service.base;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;

public interface CategoryService {

    void saveCategory(Category category);

    void saveCategories(List<Category> categories);
    
}
