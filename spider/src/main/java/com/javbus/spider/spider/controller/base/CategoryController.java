package com.javbus.spider.spider.controller.base;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.service.base.CategoryService;
import com.javbus.spider.spider.utils.R;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
@RequestMapping("category")
public class CategoryController {
    @Autowired
    private CategoryService categoryService;

    @PostMapping("save")
    public R saveCategory(@RequestBody List<Category> categories) {
        // TODO: process POST request
        if (categories == null || categories.isEmpty()) {
            return R.error();
        }
        categoryService.saveCategories(categories);
        return R.ok();
    }
    @GetMapping("query/id/{id}")
    public R queryCategoryById(@PathVariable Integer id) {
        Category category=categoryService.queryCategoryById(id);
        return R.ok().put("category", category);
    }
    @GetMapping("query/name/{name}")
    public R queryCategoryByName(@PathVariable String name) {
        Category category=categoryService.queryCategoryByName(name);
        return R.ok().put("category", category);
    }
}
