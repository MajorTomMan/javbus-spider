package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Movie;

import lombok.Data;
@Data
public class MovieCategoryVo {
    private Movie movie;
    private List<Category> categories;
}
