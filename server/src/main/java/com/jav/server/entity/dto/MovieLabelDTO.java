package com.jav.server.entity.dto;

import com.jav.server.entity.base.Label;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieLabelDTO {
    private Movie movie;
    private Label label;
}
