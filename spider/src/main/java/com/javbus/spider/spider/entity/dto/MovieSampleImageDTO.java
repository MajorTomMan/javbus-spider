package com.javbus.spider.spider.entity.dto;

import java.util.List;

import com.javbus.spider.spider.entity.base.Movie;
import com.javbus.spider.spider.entity.base.SampleImage;

import lombok.Data;

@Data
public class MovieSampleImageDTO {
    private Movie movie;
    private List<SampleImage> sampleImages;
}
