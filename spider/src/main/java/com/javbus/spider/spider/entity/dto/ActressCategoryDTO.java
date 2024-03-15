package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressCategoryDTO {
    private List<Actress> actress;
    private List<Category> categories;
}
