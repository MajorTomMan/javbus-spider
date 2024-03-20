package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Genre;

import lombok.Data;

@Data
public class GenreCategoryVO {
    Genre genre;
    List<Category> categories;
}
