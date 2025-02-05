package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Movie;

import lombok.Data;
@Data
public class MovieCategoryVO {
    Movie movie;
    List<Category> categories;
}
