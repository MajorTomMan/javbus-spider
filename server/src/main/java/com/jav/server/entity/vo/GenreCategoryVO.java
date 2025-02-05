package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Genre;

import lombok.Data;

@Data
public class GenreCategoryVO {
    Genre genre;
    List<Category> categories;
}
