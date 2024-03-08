package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;

import lombok.Data;
@Data
public class MovieCategoryVo {
    private String code;
    private List<Category> categories;
}
