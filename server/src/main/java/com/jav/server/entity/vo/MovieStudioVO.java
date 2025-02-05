package com.jav.server.entity.vo;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Studio;

import lombok.Data;


@Data
public class MovieStudioVO {
    Movie movie;
    Studio studio;
}
