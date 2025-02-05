package com.jav.server.service.base.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jav.server.dao.base.CategoryDao;
import com.jav.server.entity.base.Category;
import com.jav.server.service.base.CategoryService;

@Service
public class CategoryServiceImpl implements CategoryService{
    @Autowired
    private CategoryDao categoryDao;
    @Override
    public void saveCategory(Category category) {
        // TODO Auto-generated method stub
        categoryDao.saveCategory(category);
    }
    @Override
    public void saveCategories(List<Category> categories) {
        // TODO Auto-generated method stub
        categoryDao.saveCategories(categories);
    }
    @Override
    public Category queryCategoryById(Integer id) {
        // TODO Auto-generated method stub
        return categoryDao.queryCategoryById(id);
    }
    @Override
    public Category queryCategoryByName(String name) {
        // TODO Auto-generated method stub
        return categoryDao.queryCategoryByName(name);
    }
    
}
