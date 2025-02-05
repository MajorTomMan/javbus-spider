package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Category;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class ActressCategoryDTO {
    private List<Actress> actress;
    private List<Category> categories;
}
