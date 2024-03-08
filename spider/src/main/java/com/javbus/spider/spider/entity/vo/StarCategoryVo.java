package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Star;

import lombok.Data;

@Data
public class StarCategoryVo {
    private List<Star> stars;
    private List<Category> categories;
}
