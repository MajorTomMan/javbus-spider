package com.jav.server.entity.vo;

import com.jav.server.entity.base.BigImage;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieBigImageVO {
    Movie movie;
    BigImage bigImage;
}
