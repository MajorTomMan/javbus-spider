package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Genre;

import lombok.Data;

@Data
public class GenreCategoryDTO {
    private Genre genre;
    private List<Category> categories;
}
