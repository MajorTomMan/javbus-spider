package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Genre;

import lombok.Data;

@Data
public class GenreCategoryVo {
    private Integer id;
    private Genre genre;
    private List<Category> categories;
}
