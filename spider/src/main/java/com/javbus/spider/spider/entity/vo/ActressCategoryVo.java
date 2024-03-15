package com.javbus.spider.spider.entity.vo;

import java.util.List;

import com.javbus.spider.spider.entity.base.Category;
import com.javbus.spider.spider.entity.base.Actress;

import lombok.Data;

@Data
public class ActressCategoryVO {
    Actress actress;
    List<Category> categories;
}
