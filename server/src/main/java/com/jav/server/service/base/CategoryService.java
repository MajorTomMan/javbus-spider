package com.jav.server.service.base;

import java.util.List;

import com.jav.server.entity.base.Category;

public interface CategoryService {

    void saveCategory(Category category);

    void saveCategories(List<Category> categories);

    Category queryCategoryById(Integer id);

    Category queryCategoryByName(String name);
    
}
