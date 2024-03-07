package com.javbus.spider.spider.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.Category;
import com.javbus.spider.spider.service.CategoryService;
import com.javbus.spider.spider.utils.R;

@RestController
@RequestMapping("category")
public class CategoryController {
    @Autowired
    private CategoryService categoryService;
    
    @PostMapping("save")
    public R saveCategory(@RequestBody Category category) {
        // TODO: process POST request
        categoryService.saveCategory(category);
        return R.ok();
    }
}
