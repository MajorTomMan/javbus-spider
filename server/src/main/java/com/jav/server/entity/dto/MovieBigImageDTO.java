package com.jav.server.entity.dto;

import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieBigImageDTO {
    private Movie movie;
    private BigImage bigImage;
}
