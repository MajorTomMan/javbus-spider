package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Genre;

import lombok.Data;

@Data
public class GenreCategoryDTO {
    private Genre genre;
    private List<Category> categories;
}
