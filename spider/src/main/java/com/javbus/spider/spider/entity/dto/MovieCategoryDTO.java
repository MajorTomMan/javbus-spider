package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;
@Data
public class MovieCategoryDTO {
    private Movie movie;
    private List<Category> categories;
}
