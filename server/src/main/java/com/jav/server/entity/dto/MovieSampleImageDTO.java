package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Movie;
import com.jav.server.entity.base.SampleImage;

import lombok.Data;

@Data
public class MovieSampleImageDTO {
    private Movie movie;
    private List<SampleImage> sampleImages;
}
