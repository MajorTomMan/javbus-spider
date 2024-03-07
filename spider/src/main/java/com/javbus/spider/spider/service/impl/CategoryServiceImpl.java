package com.javbus.spider.spider.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.javbus.spider.spider.dao.CategoryDao;
import com.javbus.spider.spider.entity.Category;
import com.javbus.spider.spider.service.CategoryService;

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
    
}
