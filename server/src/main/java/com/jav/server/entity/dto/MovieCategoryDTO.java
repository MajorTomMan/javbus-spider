package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Movie;

import lombok.Data;
@Data
public class MovieCategoryDTO {
    private Movie movie;
    private List<Category> categories;
}
