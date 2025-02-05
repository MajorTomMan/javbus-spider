package com.jav.server.entity.dto;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Studio;

import lombok.Data;


@Data
public class MovieStudioDTO {
    private Movie movie;
    private Studio studio;
}
