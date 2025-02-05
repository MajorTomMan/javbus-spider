package com.jav.server.entity.vo;

import java.util.List;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.SampleImage;

import lombok.Data;

@Data
public class MovieSampleImageVO {
    Movie movie;
    List<SampleImage> sampleImages;
}
