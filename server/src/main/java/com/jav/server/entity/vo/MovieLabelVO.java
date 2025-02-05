package com.jav.server.entity.vo;

import com.jav.server.entity.base.Label;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieLabelVO {
    Movie movie;
    Label label;
}
