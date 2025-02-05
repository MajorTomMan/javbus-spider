package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.Actress;

import lombok.Data;

@Data
public class MovieActressVO {
    Movie movie;
    List<Actress> actresses;
}
