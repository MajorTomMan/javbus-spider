package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class ActressCategoryVO {
    Actress actress;
    List<Category> categories;
}
